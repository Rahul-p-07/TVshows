from flask import Flask,render_template,request,redirect,url_for
import requests


app=Flask("myApp")

@app.route("/", methods=["POST","GET"])
def serachshows():
    if request.method == "POST":
        q=request.form["query"]
        return redirect(url_for("display" , query=q))
    else:
        return render_template("searchbar.html")

@app.route("/search=<query>")
def display(query):
    response = requests.get(f"https://api.tvmaze.com/search/shows?q={query}")
    data=response.json()
    if len(data)==0:
        return f"<header> No related shows </header>"
    else:
        extracted_data = []
        for item in data:
            show_info = {
                "name": item["show"]["name"],
                "language": item["show"]["language"],
                "genres": item["show"]["genres"],
                "rating": item["show"]["rating"]["average"],
                "summary": item["show"]["summary"],
            }
            if item["show"]["image"] is None:
                show_info["image"] = "https://via.placeholder.com/150"
            else:
                show_info["image"] = item["show"]["image"]["medium"]
            extracted_data.append(show_info)
        return render_template("res2.html", shows=extracted_data)
if __name__ == '__main__':
    app.run(debug=True)