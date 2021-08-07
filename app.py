from flask import Flask, request, render_template
from wordcloud import WordCloud


import base64
import matplotlib.pyplot as plt
import io


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        file = request.files['file']
        origin = file.filename
        txt = file.read().decode('utf-8')
        print(type(txt))
            # .replace('\n','')

        stopwords = request.form['stop_words']

        if stopwords:
            stopwords = stopwords.split(',')

        return generate_word_cloud(txt, stopwords=stopwords, origin=origin)


def generate_word_cloud(txt, stopwords=None, origin=None):
    wordcloud = WordCloud(random_state=8,
                          normalize_plurals=False,
                          width=600, height=300,
                          max_words=50,
                          stopwords=stopwords)
    wordcloud.generate(txt)

    s = io.BytesIO()

    # create a figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 6))

    # add interpolation = bilinear to smooth things out

    plt.imshow(wordcloud, interpolation='bilinear')
    # and remove the axis

    plt.axis("off")

    plt.savefig(s, format='png', bbox_inches='tight')

    plt.close()

    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

    return render_template('index.html', result=s, excluded=stopwords, origin=origin)


if __name__ == '__main__':
    app.run(debug=True)