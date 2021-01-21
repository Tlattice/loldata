import matplotlib as plt
import tensorflow as tf

model = tf.keras.models.load_model('output/predictive_model.model')
test_predictions_baseline = model.predict(test_features, batch_size=BATCH_SIZE)


cm = confusion_matrix(labels, predictions > p)
print('Legitimate Transactions Detected (True Negatives): ', cm[0][0])
print('Legitimate Transactions Incorrectly Detected (False Positives): ', cm[0][1])
print('Fraudulent Transactions Missed (False Negatives): ', cm[1][0])
print('Fraudulent Transactions Detected (True Positives): ', cm[1][1])
print('Total Fraudulent Transactions: ', np.sum(cm[1]))
