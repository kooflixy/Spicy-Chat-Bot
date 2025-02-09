import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename=".log",filemode="a", encoding='utf-8',
                        format="%(asctime)s %(levelname)s %(message)s")
    
    print('start')