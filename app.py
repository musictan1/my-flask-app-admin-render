from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 관리자 홈 → 대시보드
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# 로그인 페이지
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 여기서는 예시로 간단히 처리 (실제 사용시 보안 추가 필요)
        if username == "admin" and password == "password":
            return redirect(url_for("dashboard"))
        else:
            return "Login Failed", 401

    return render_template("login.html")

# 앱 실행
if __name__ == "__main__":
    app.run(debug=True)
