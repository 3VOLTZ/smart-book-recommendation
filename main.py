from tkinter import *
from tkinter import messagebox
import requests
from PIL import ImageTk, Image
from io import BytesIO
import urllib.parse

class Request:
    def __init__(self, method, args):
        self.args = args
        self.method = method

inc = 0
startIndex = 0
current_search_term = ""

def fetch_information(title, image, date, rating):
    global inc
    inc += 1

    text[f'a{inc}'].config(text=title)
    if check_var.get():
        text2[f'a{inc}{inc}'].config(text=date)
    else:
        text2[f'a{inc}{inc}'].config(text="")
        
    if check_var2.get():
        text3[f'a{inc}{inc}{inc}'].config(text=rating)
    else:
        text3[f'a{inc}{inc}{inc}'].config(text="")

    if image != 'N/A':
        response = requests.get(image)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        resized_image = img.resize((140, 200))
        photo2 = ImageTk.PhotoImage(resized_image)
        image_label[f'b{inc}'].config(image=photo2)
        image_label[f'b{inc}'].image = photo2

def search(next_batch=False):
    global inc, startIndex, current_search_term
    if not next_batch:
        inc = 0
        startIndex = 0
        current_search_term = Search.get()
    else:
        inc = 0
        startIndex += 5

    request = Request('GET', {'search': current_search_term})

    if request.method == 'GET':
        search = urllib.parse.quote(request.args.get('search', ''))
        url = f"https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=5&startIndex={startIndex}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', 'N/A')
                date = volume_info.get('publishedDate', 'N/A')
                rating = volume_info.get('averageRating', 'N/A')
                image_links = volume_info.get('imageLinks', {})
                image = image_links.get('thumbnail', 'N/A')

                fetch_information(title, image, date, rating)

                if check_var.get() or check_var2.get():
                    frame11.place(x=160, y=600)
                    frame22.place(x=360, y=600)
                    frame33.place(x=560, y=600)
                    frame44.place(x=760, y=600)
                    frame55.place(x=960, y=600)
                else:
                    frame11.place_forget()
                    frame22.place_forget()
                    frame33.place_forget()
                    frame44.place_forget()
                    frame55.place_forget()
        else:
            print("Failed to load data from Google Books API")
            messagebox.showinfo("info", "Failed to load data from Google Books API")

def refresh_books():
    search(next_batch=True)

def show_menu(event):
    # display menu at mouse position
    menu.post(event.x_root, event.y_root)

def logout():
    root.destroy()

root = Tk()
root.title("Book Recommendation System")
root.geometry("1250x700+200+100")
root.config(bg="#F8E1E1")
root.resizable(False, False)

# icon
icon_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\icon.png")
root.iconphoto(False, icon_image)

# background image
heading_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\background.png")
Label(root, image=heading_image, bg="#111119").place(x=-2, y=-2)

# logo
logo_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\logo.png")
Label(root, image=logo_image, bg="#F8E1E1").place(x=300, y=80)

# heading
heading = Label(root, text="Book Recommendation System", font=("Elephant", 30, "bold"))
heading.place(x=410, y=90)

# search box background image
search_box = PhotoImage(file="E:\\book_recommendation_system\\Images\\Rectangle 2.png")
Label(root, image=search_box, bg="#0099ff").place(x=400, y=155)

# search box
Search = StringVar()
search_entry = Entry(root, textvariable=Search, width=20, font=("Lato", 25), bg="white", fg="black", bd=0)
search_entry.place(x=512, y=172)

# search button
recommend_button_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\Search.png")
recommend_button = Button(root, image=recommend_button_image, bg="#0099ff", bd=0, activebackground="#252532", cursor="hand2", command=search)
recommend_button.place(x=860, y=169)

# refresh button
Refresh_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\refresh.png")
refresh = Button(root, image=Refresh_image, bd=0, cursor="hand2", activebackground="#F8E1E1", bg="#0099ff", command=refresh_books)
refresh.place(x=350, y=175)

# setting button
Setting_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\setting.png")
setting = Button(root, image=Setting_image, bd=0, cursor="hand2", activebackground="#F8E1E1", bg="#0099ff")
setting.place(x=1000, y=175)
setting.bind('<Button-1>', show_menu)

menu = Menu(root, tearoff=0)  # search menu

check_var = BooleanVar()
menu.add_checkbutton(label="Publish Date", variable=check_var, command=lambda: print(f"check Option is {'checked' if check_var.get() else 'unchecked'}"))

check_var2 = BooleanVar()
menu.add_checkbutton(label="Ratings", variable=check_var2, command=lambda: print(f"check Option is {'checked' if check_var2.get() else 'unchecked'}"))

# logout button
Logout_image = PhotoImage(file="E:\\book_recommendation_system\\Images\\logout.png")
Button(root, image=Logout_image, bd=0, cursor="hand2", activebackground="#0099ff", bg="white", command=logout).place(x=1200, y=650)

# frames for book information
frame1 = Frame(root, width=150, height=240, bg="white", borderwidth=2, relief="solid")
frame2 = Frame(root, width=150, height=240, bg="white", borderwidth=2, relief="solid")
frame3 = Frame(root, width=150, height=240, bg="white", borderwidth=2, relief="solid")
frame4 = Frame(root, width=150, height=240, bg="white", borderwidth=2, relief="solid")
frame5 = Frame(root, width=150, height=240, bg="white", borderwidth=2, relief="solid")
frame1.place(x=160, y=350)
frame2.place(x=360, y=350)
frame3.place(x=560, y=350)
frame4.place(x=760, y=350)
frame5.place(x=960, y=350)

# book titles
text = {
    'a1': Label(frame1, text="Book Title", font=("arial", 10, "bold"), fg="green", bg="white"),
    'a2': Label(frame2, text="Book Title", font=("arial", 10, "bold"), fg="green", bg="white"),
    'a3': Label(frame3, text="Book Title", font=("arial", 10, "bold"), fg="green", bg="white"),
    'a4': Label(frame4, text="Book Title", font=("arial", 10, "bold"), fg="green", bg="white"),
    'a5': Label(frame5, text="Book Title", font=("arial", 10, "bold"), fg="green", bg="white")
}
text['a1'].place(x=10, y=4)
text['a2'].place(x=10, y=4)
text['a3'].place(x=10, y=4)
text['a4'].place(x=10, y=4)
text['a5'].place(x=10, y=4)

# book covers
image_label = {
    'b1': Label(frame1),
    'b2': Label(frame2),
    'b3': Label(frame3),
    'b4': Label(frame4),
    'b5': Label(frame5)
}
image_label['b1'].place(x=3, y=30)
image_label['b2'].place(x=3, y=30)
image_label['b3'].place(x=3, y=30)
image_label['b4'].place(x=3, y=30)
image_label['b5'].place(x=3, y=30)

# frames for additional book information (date and ratings)
frame11 = Frame(root, width=150, height=50, bg="white", borderwidth=2, relief="solid")
frame22 = Frame(root, width=150, height=50, bg="white", borderwidth=2, relief="solid")
frame33 = Frame(root, width=150, height=50, bg="white", borderwidth=2, relief="solid")
frame44 = Frame(root, width=150, height=50, bg="white", borderwidth=2, relief="solid")
frame55 = Frame(root, width=150, height=50, bg="white", borderwidth=2, relief="solid")

# dates of publication
text2 = {
    'a11': Label(frame11, text="Date", font=("arial", 10), bg="#e7e7e7"),
    'a22': Label(frame22, text="Date", font=("arial", 10), bg="#e7e7e7"),
    'a33': Label(frame33, text="Date", font=("arial", 10), bg="#e7e7e7"),
    'a44': Label(frame44, text="Date", font=("arial", 10), bg="#e7e7e7"),
    'a55': Label(frame55, text="Date", font=("arial", 10), bg="#e7e7e7")
}
text2['a11'].place(x=10, y=4)
text2['a22'].place(x=10, y=4)
text2['a33'].place(x=10, y=4)
text2['a44'].place(x=10, y=4)
text2['a55'].place(x=10, y=4)

# ratings
text3 = {
    'a111': Label(frame11, text="Ratings", font=("arial", 10), bg="#e7e7e7"),
    'a222': Label(frame22, text="Ratings", font=("arial", 10), bg="#e7e7e7"),
    'a333': Label(frame33, text="Ratings", font=("arial", 10), bg="#e7e7e7"),
    'a444': Label(frame44, text="Ratings", font=("arial", 10), bg="#e7e7e7"),
    'a555': Label(frame55, text="Ratings", font=("arial", 10), bg="#e7e7e7")
}
text3['a111'].place(x=10, y=25)
text3['a222'].place(x=10, y=25)
text3['a333'].place(x=10, y=25)
text3['a444'].place(x=10, y=25)
text3['a555'].place(x=10, y=25)

root.mainloop()
