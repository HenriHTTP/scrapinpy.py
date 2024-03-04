import pandas as pd
import json
from queue import Queue
from threading import Thread


def process_normative(item, result_queue):
    # Process each item individually
    content_normative = item.get("conteudo_documento", "")
    table_data = item.get("anexo_documento", "")
    normative_title = item.get("titulo_normativo", "")
    document_url = item.get("document_url", "")
    document_signer = item.get("assinante_documento", "")
    political_bodies = item.get("orgao", "")
    release_date = item.get("data_publicacao", "")
    summary = item.get("ementa", "")

    normative_data = {
        "conteudo_documento": content_normative,
        "titulo_normativo": normative_title,
        "document_url": document_url,
        "assinante_documento": document_signer,
        "orgao": political_bodies,
        "data_publicacao": release_date,
        "anexo_documento": table_data,
        "ementa": summary
    }
    print(normative_data)
    result_queue.put(normative_data)


def process_normative_queue(input_queue: Queue, result_queue: Queue) -> None:
    # Process the item queue
    while True:
        normative_item = input_queue.get()
        if normative_item is None:
            break
        process_normative(normative_item, result_queue)
        input_queue.task_done()


async def convert_json_to_csv(json_file_path: str, csv_output_path: str) -> None:
    try:
        with open(json_file_path, 'r') as json_file:
            normative_data = json.load(json_file)

        if not isinstance(normative_data, list):
            raise ValueError("Invalid JSON format. Expected a list of dictionaries.")

        result_queue = Queue()
        input_queue = Queue()
        num_threads = 4
        threads = []

        def start_processing_threads():
            for _ in range(num_threads):
                thread = Thread(target=process_normative_queue, args=(input_queue, result_queue))
                thread.start()
                threads.append(thread)

        def wait_for_processing_threads():
            for _ in range(num_threads):
                input_queue.put(None)
            for thread in threads:
                thread.join()

        start_processing_threads()

        for normative_item in normative_data:
            input_queue.put(normative_item)

        input_queue.join()
        wait_for_processing_threads()

        processed_normative = []
        while not result_queue.empty():
            processed_normative.append(result_queue.get())

        normative_dataframe = pd.DataFrame.from_records(processed_normative)

        if "conteudo_documento" in normative_dataframe.columns:
            normative_dataframe = pd.concat(
                [normative_dataframe.drop(columns=['conteudo_documento']),
                 pd.DataFrame(normative_dataframe['conteudo_documento'].tolist(), index=normative_dataframe.index)],
                axis=1
            )

        normative_dataframe.to_csv(csv_output_path, index=False)
        print(f"CSV generated successfully. File path: '{csv_output_path}'")

    except Exception as e:
        raise ValueError(f"Error: {e}")
