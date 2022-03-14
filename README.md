# Digikala Supercup
My solutions for Data Science problems in [Digikala Supercup (March 2022)](https://quera.org/events/digikala-datascience-0012).

## Preparation
**Q1 (NLP)**: Predicting the price of products based on their categorical and text features.\
**Solution**: Used Bidirectional GRU + MLP components to predict the price as a regression problem.\
\
**Q2 (Vision)**: Detecting if the image of a product has watermark. \
**Solution**: Fine-tuned EfficientNet on the given task.\
\
**Q3 (Time Series)**: Predicting the next time a user will buy a certain product.\
**Solution**: Extracted a set of features from the data (frequency of purchase, days between purchases, etc.) and used Ridge Regression to predict the next purchase date.\
\
**Q4 (Algorithm)**: A simple algorithm problem.\
**Q5 (Database)**: Calculating nDCG on search results.

## Final Competition
Design and implementation of a system to recommend shops and products to customers.

**Solution**:
1. *Filter* the shops in the vicinity of the customer and list the product they sell.
2. *Score* the shops/products based on their overal rating and popularity + previous orders of the user (the ratings, categories the user mostly buys from, etc.).
3. *Sort* the shops/products based on the score calculated above.
