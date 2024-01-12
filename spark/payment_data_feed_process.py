import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from cryptography.fernet import Fernet


spark = SparkSession.builder.appName("PaymentsTransformation").getOrCreate()

def decode(encoded_used_id: bytes) -> str:
    key = b'CuTaE-KQM5MOZkExifXvfssUzXxU4TtNQyiggxCh8G8='
    used_id: str = Fernet(key).decrypt(encoded_used_id.decode()).decode()
    return used_id

# Read the payments data  parquet file 
payments_df = spark.read.parquet("/input/payments-input.snappy.parquet", header=True)
payments_df.show()

# 1. Show the total sum amount for each currency
currency_sums = payments_df.groupBy("currency").sum("amount")
currency_sums.show()

# 2. Create exchange rates DataFrame and add amount_in_ils column
exchange_rates_df = spark.createDataFrame([
    ("USD", 4.0),
    ("EUR", 3.7)
], ["currency", "rate_to_ils"])

payments_with_ils = payments_df.join(exchange_rates_df, on="currency") \
                               .withColumn("amount_in_ils", F.col("amount") * F.col("rate_to_ils"))

# 3. Decrypt encoded_user_id column
key = b'your_decryption_key'
payments_with_ils = payments_with_ils.withColumn("user_id", decode(F.col("encoded_user_id")))

payments_with_ils.show()

spark.stop()
