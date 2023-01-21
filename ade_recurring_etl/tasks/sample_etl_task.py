from ade_recurring_etl.common import Task
from sklearn.datasets import fetch_california_housing
import pandas as pd


class SampleETLTask(Task):
    def __init__(self, spark=None, init_conf=None):
        super(SampleETLTask, self).__init__(spark, init_conf)
        if not bool(self.conf):
          self.conf = {
            "output": {
              "database": "default",
              "table": "sklearn_housing"
            }
          }  
    def _write_data(self):
        db = self.conf["output"].get("database", "default")
        table = self.conf["output"]["table"]
        self.logger.info(f"Writing housing dataset to {db}.{table}")
        _data: pd.DataFrame = fetch_california_housing(as_frame=True).frame
        df = self.spark.createDataFrame(_data)
        df.write.format("delta").mode("overwrite").saveAsTable(f"{db}.{table}")
        self.logger.info("Dataset successfully written")
        _data2: pd.DataFrame = self.spark.table(f"{db}.{table}").toPandas()
        print(len(_data2))

    def launch(self):
        self.logger.info("Launching sample ETL task")
        self._write_data()
        self.logger.info("Sample ETL task finished!")

# if you're using python_wheel_task, you'll need the entrypoint function to be used in setup.py
def entrypoint():  # pragma: no cover
    task = SampleETLTask()
    task.launch()

# if you're using spark_python_task, you'll need the __main__ block to start the code execution
if __name__ == '__main__':
    entrypoint()
