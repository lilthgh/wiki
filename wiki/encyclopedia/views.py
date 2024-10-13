from django.shortcuts import render,redirect
import markdown
from . import util
from django.http import HttpResponseRedirect
import random

def md_html(title):
    markdowner =markdown.Markdown()
    entryPage =util.get_entry(title)
    if entryPage == None:
        return None
    else:
        return markdowner.convert(entryPage)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    html_content = md_html(title)
    
    if html_content is None:
        return render(request,"encyclopedia/error.html",{
            "message":"Does not exist"}) 

    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            
            "content": html_content
        })
def search(request):
    if request.method=="POST":
        entry_request =request.POST['q']
        html_content =md_html(entry_request)
        if html_content is None:
            recommendations=[]
            for entry in util.list_entries():
                if entry_request.upper() in entry.upper():
                    recommendations.append(entry)
            return render(request,"encyclopedia/search.html",{
                        "recommendations": recommendations 
            })
        else:
            title = entry_request  # Assuming title should be the requested entry  
            content = html_content
            return render(request,"encyclopedia/entry.html",{
            "title":title,
            
            "content": content
        })
def new(request):  
    if request.method == "POST":  
        title = request.POST['title']  
        content = request.POST['content']  

        # Check for duplicate title  
        existing_entry = util.get_entry(title)   
        if existing_entry is None:  
            # Save the new entry  
            util.save_entry(title, content)  
            html_content = md_html(content)  
            # Store the title in the session private 
            request.session['last_created_entry'] = title 
            return redirect("entry", title=title)    
        
        else:  
            return render(request, "encyclopedia/error.html", {  
                "message": "Duplicate Title"  
            })  
    else:          
        last_created_entry = request.session.get('last_created_entry')  
        return render(request, "encyclopedia/new.html", {  
            "last_created_entry": last_created_entry,  
        })
def edit(request):
    if request.method =="POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title) 
        
        return render(request,"encyclopedia/edit.html",{
            "title": title,
            "content":content} )
def save_edit(request):
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        util.save_entry(title,content)
        html_content = md_html(title) 
        return render(request,"encyclopedia/entry.html",{
            "title": title,
            "content":html_content} )

def rand(request):
    Entries=util.list_entries()
    rand_choice=random.choice(Entries)
    html_content = md_html(rand_choice)
    return render(request,"encyclopedia/entry.html",{
            "title":rand_choice,
            "content":html_content} )

        

 