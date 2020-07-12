from django.shortcuts import render
from django.http import HttpResponse
import markdown2 as md
from django import forms
from django.core.files import File
import os
import random

from . import util

class NewEntryForm(forms.Form):
	title = forms.CharField(label="Title")
	entry = forms.CharField(widget=forms.Textarea())

def index(request):
	return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def wikipage(request, title):
	try:
		entry= md.markdown(util.get_entry(title))
		return render(request, "encyclopedia/wikipage.html", {"title":title, "entry":entry })
	except: 
		return render(request, "encyclopedia/error.html", {"message":"Wikipage not found" })

def search(request):
	if request.method == "POST":
		input = dict(request.POST)["q"][0].lower()
		if input in [entry.lower() for entry in util.list_entries()]:
			entry= md.markdown(util.get_entry(input)) 
			return render(request, "encyclopedia/wikipage.html", {"title":input, "entry":entry })
		else: 
			entries = []
			for entry in util.list_entries():
				if input in entry.lower(): 
					entries.append(entry)
			return render(request, "encyclopedia/search.html", {"entries": entries})
	else:
		return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def new(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			entry_in = form.cleaned_data["entry"]

			if title.lower() not in [entry.lower() for entry in util.list_entries()]: 
				filename = f"{title}.md"
				module_dir = os.path.dirname("./entries/")
				f = open(os.path.join(module_dir, filename), "x")
				myfile = File(f)
				entry= f"# {title} \n \n {entry_in}"
				myfile.write(entry)
				myfile.closed
				f.close()
				
				return render(request, "encyclopedia/wikipage.html", {"title":title, "entry":md.markdown(entry)})
			else:
				return render(request, "encyclopedia/error.html", {"message":"Wikipage already exists" })


	return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})

def edit(request, title):
	entry = util.get_entry(title).split("\n")[2:]

	input = {"title": title, "entry": entry[0]}
	return render(request,"encyclopedia/edit.html", {"form": NewEntryForm(input)})

def edited(request):
	if request.method == "POST":
		form = NewEntryForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			entry_in = form.cleaned_data["entry"]

			if title.lower() in [entry.lower() for entry in util.list_entries()]: 
				filename = f"{title}.md"
				module_dir = os.path.dirname("./entries/")
				f = open(os.path.join(module_dir, filename), "w")
				entry= f"# {title} \n \n {entry_in}"
				f.write(entry)
				f.closed
				f.close()
				
				return render(request, "encyclopedia/wikipage.html", {"title":title, "entry":md.markdown(entry)})
			else:
				return render(request, "encyclopedia/error.html", {"message":"Title was changed" })

def random_page(request):
	title = random.choice(util.list_entries())
	entry= md.markdown(util.get_entry(title))
	return render(request, "encyclopedia/wikipage.html", {"title":title, "entry":entry })