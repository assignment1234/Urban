import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', arguments={'x-max-priority': 10})

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!',
                      properties=pika.BasicProperties(priority=5))



channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World! Mukul',
		      properties=pika.BasicProperties(priority=1))
print(" [x] Sent 'Hello World!'")
connection.close()
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body=str(t.id),
#                       properties=pika.BasicProperties(priority=5))

