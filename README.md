# Stark tech test

## 數據處理
#### 執行**data_process.py**後可以把**output_clean_date_technical.json**扁平化，包含四個csv:
1.  financial_growth.csv : 季度增長率的資料
2.  historical_prices.csv : 歷史股價的資料
3.  merged_data.csv : 將兩個資料做outer join
4.  data.csv : 作為後面訓練用資料集，將財報資料更新到發布以後到下一個財報發行之前的日期，同時加入與財報發布日期的差距作為權重，沒有財報的前12筆資料則捨棄掉，處理過後的資料只剩下財報發布但股市未開的日子有缺值，因預測目標為股市價格，也將該日期捨棄。
##    模型訓練及選用問題

### 1.    如果要達成「能夠預測指定的symbol在90天後，是否有成長10%」的目標，會選用的模型及訓練方式。
#### Ans: 
1. SVM : SVM適合用來做二元判斷式，且擅長處理高維度資料，在訓練上須使用grid search來交叉驗證最佳參數  
2. RF : RF 是一種集成學習方法，通過多個決策樹的投票來進行分類，對異常值具有較好的resistance，訓練上比較不需要要調整參數，因為其集成的性質，performance通常相對穩定。

###  2.    在訓練中如何從現有的資料及提取出關鍵影響欄位。
#### Ans:
1. 特徵相關性分析:通過分析這些指標之間的相關性，可以找出對股票價格影響較大的財務指標。  
2. 特徵重要性分析:主要是用在RandomForest中，可以透過gini係數來判斷可以獲得的信息量。  
3. Field Knowlegde:查詢相關資料可以判斷出那些特徵可能對股價有影響，舉例來說，成交量是促成價格動能的關鍵，沒有動能價格就不會變動。


### 3.    如何利用目前已有的資料集欄位，推論出更有效的新資料欄位
#### Ans:
1. 財報部位新增與財報發布日的天數差距，來降低長期的影響，避免資料都歸一化，並且根據天數來重新計算成長率。  
2. 為了更精準的預測，把過去一段時間的資料也統整成特徵來做為參考  
    * 15MA : 過去15天的價格平均。  
    * 30MA : 過去30天的價格平均。  
    * RSI : 相對價格強弱指標，透過比較過去一段時間價格變動的平均值來判斷買賣壓力的比較，愈大代表過去購買力道愈強，通常過高或過低代表出現背離(>70% or <30%)，也能作為判斷依據。  
    * MACD : 移動平均線收斂與發散指標，由MACD和信號線組成，MACD線高於信號線時通常代表價格會上漲，可以做為趨勢的判斷。  

    以上指標有助於幫助建構一段時間內的資料，確切的時間範圍設定可以根據投資週期另行設定。

## Insight and Observation
1. 大多數成長率的參數都高度正相關，因此在實際訓練時我只保留了投資人較常看的收益成長率和毛利率等，可能會因此喪失一些資訊，這方面仍需更嚴謹的觀察。
2. Randomforest的結果高得離譜，再用decision tree來檢查篩選結果時可以發現，在台泥過去的資料中有一段時間(疫情中)股價跌得很低，因此只要選擇在這個時期進場，就能達到高收益，在機器學習的角度看來就是overfitting，再投資的角度來說，若進行的是左側交易，也就是希望可以買在股票下跌的終點，跑完整個上漲波段來說的話，確實就是該鎖定價格出現離群值的低點，因此這個模型才能有這麼好的效果。  
3. SVM的表現相對較弱，但是我認為主要分開資料的應該參數也是價格相關，但是透過其他參數使模型較為平滑。