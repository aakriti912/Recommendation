from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
vehicles = pickle.load(open('vehicles.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('/index.html',
                           vehicle_name = list(popular_df['vehicle.model'].values),
                           owner=list(popular_df['owner.id'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('/recommend.html')

@app.route('/recommend_vehicles',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==vehicle_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = vehicles[vehicles['vehicle.model'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('vehicle.model')['vehicle.model'].values))
        item.extend(list(temp_df.drop_duplicates('vehicle.model')['fuelType'].values))
        item.extend(list(temp_df.drop_duplicates('vehicle.model')['vehicle.make'].values))
        
        data.append(item)
    

    print(data)

    return render_template('/recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)