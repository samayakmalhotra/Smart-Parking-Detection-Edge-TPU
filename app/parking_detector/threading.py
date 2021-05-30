import threading
import random
import time

from .inference import make_inference


class ThreadedInference(threading.Thread):
    def __init__(self, queue, image_table):
        threading.Thread.__init__(self)
        self.queue = queue
        self.image_table = image_table

    def run(self):
        inference_result = {}
        inference_result['empty_spaces'] = []
        inference_result['parked_spaces'] = []
        start_time = time.time()
        for slot in self.image_table.keys():
            result = make_inference(self.image_table[slot])

            if result == 'empty':
                inference_result['empty_spaces'].append(slot)
            else:
                inference_result['parked_spaces'].append(slot)
        end_time = time.time()
        elapsed_time = end_time - start_time
        inference_result['inference_time'] = elapsed_time
        self.queue.put(inference_result)
