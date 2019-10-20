# RSS-Manager 

## Table of Contents
  1. [Table of Contents](#table-of-contents)
  2. [Guide](#Guide)
      1. [Download the Program](#download-the-program)
      1. [Starting the Server](#starting-the-Server)
      2. [Starting the Generator](#starting-the-generator)
      3. [Creating a New Feed](#creating-a-new-feed)
          1. [Defining the Feed](#defining-the-feed)
          2. [Creating an Item Pattern](#creating-an-item-pattern)
          3. [Defining the Items](#defining-the-items)
      4. [Adding a Feed to Your Feed Reader](#adding-a-feed-to-your-feed-reader)
      5. [Deleting a Feed](#deleting-a-feed)
  2. [Compatible Feed Readers](#compatible-feed-readers)
  3. [Support the Developer](#support-the-developer)

## Guide

Hello, and thank you for showing interest in my RSS generator!

This generator is a standalone package that provides you with everything you need to create an RSS feed from a webpage that does not have one.

To do this it does two things:
  1. Periodically scans the webpage for updates & produces an xml file
  2. Hosts that xml file on a small, locally accessible server so that it can be read by an RSS feed reader

It should be noted that this means the generator will only work with Feed readers that are run from your machine and can access localhost. i.e. your feed reader has to be a standalone program or a browser add-on. Online feed readers are not compatible as they cannot read the xml file (unless you make a hole in your firewall and give the internet access to your computer).

A full list of compatible and incompatible readers can be found here.

### Download the Program

To begin, download the program in one of three ways:
  1. Direct Download
  2. Torrent Download
  3. Clone this Git Repository
  
<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/download.jpg">
</p>

If you opt to clone the git repo, I apologize for the mess.

Once you have downloaded the .zip file, unzip it and you should have a folder with the following contents:
  - Feeds folder
  - Img folder
  - Pages folder
  - Feed_Definitions.txt
  - Generator.exe
  - Server.exe
  
<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/unzip.jpg">
</p>
  
If that is correct, you are ready to begin.



*****

### Starting the Server

The first step is to start up the server.

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/server.jpg">
</p>

In addition to serving the .xml file to your feed reader, the server provides a user-friendly web interface for the generator. 

To start the server, simply open the server.exe file.

The program will tell you your local IP address and will ask you if you want to use the default port number (in this case port 8000). If you choose not to use port 8000 it will ask you to choose a new port be 1 and 65535.

The server will then start up. It will be accessible to your machine at [localhost:8000](localhost:8000) and will be accessible to other computers on your LAN network. 

If you open a web browser and go to [localhost:8000](localhost:8000) you should see something like the image below. 

If that is the case, you have correctly set up the server. 

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/home.jpg">
</p>

*****

### Starting the Generator

To start the generator, simply open generator.exe. It should look like this: 

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/generator.jpg">
</p>

*****

### Creating a New Feed

To create a feed, simply go to the “New Feed” page and follow the instructions to fill out the form. Creating a new feed is the most difficult part of using the program, so if you have any questions you can refer to this document, mouse over a field for an explanation, or visit the RSS official documentation.

Creating a new Feed is broken into three parts:
  1.	Defining the feed
  2.	Creating an item pattern
  3.	Defining the items
  
To explain how to add a feed, I will provide a walkthrough using the YouTube trending page as an example. Ultimately the feed should mimic the trending page and provide us with an update when a new video hits the trending page. 

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/youtube.jpg">
</p>

#### Defining the Feed

Defining the feed is simply giving some basic information about the feed such as a name, and a description. We’ll also add a link, which is where the feed will pull the data from. In this case, our link is the youtube trending page: https://www.youtube.com/feed/trending.

The feed TTL is how long the feed reader should wait before checking for updates from the feed. It is essentially how often the feed updates. The default setting is 60 minutes. 

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/basic.jpg">
</p>

#### Creating an Item Pattern

For the purpose of our feed we need the generator to convert videos on the trending page, into items in our feed. We do this by making an "Item Pattern".

If you look at the videos, they all have common traits:
-	Title
-	Length
-	Creator
-	Description
-	View Count
-	URL
-	Upload Time

Each video will have these traits defined in the page's HTML data. Our Item Pattern is just a text pattern that will tell the generator where in the HTML these traits are defined. 

Producing a pattern is simple, we just need to take an item and replace all of its item-unique text with placeholders that the generator can match to every item (video) in the feed. The easiest way to do this is to compare it with another item.

To start, click the “Scrape URL” button, and watch as the “Scraped Page Source Data” box fills up. This box contains the raw HTML for the webpage we gave earlier in the “Feed Link” field.

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/first.jpg">
</p>

If we look at the YouTube trending page, we’ll see that the first video is entitled “Sooubway 4: The Final Sandwich”. We’ll scroll through the source data, looking for HTML that mentions this item.

Once we find it, we will copy and paste it into a text-comparison software like https://text-compare.com/. We only want to copy the text for one item, but we want to make sure we get all the data we need: title, length, description, etc.

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/compare.jpg">
</p>

Then we find another item and compare the two texts. The highlighted areas are text that needs to be a placeholder in our pattern, either as {%} for data we want, or {\*} for data we don't. The highlighted areas will likely be in quotation marks, and in that case the entire content in the quotes probably has to be replaced with a placeholder. 

In the end we come out with a pattern like so:

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/pattern.jpg">
</p>
 
Which produces the following result:
 
<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/result.jpg">
</p>
 
As you can see, our {%} placeholders have been numbered and are storing the following data:
- {%1}: video ID
- {%2}: Title
- {%3}: Video Duration
- {%4}: Channel URL
- {%5}: Channel Name
- {%6}: Publish Time
- {%7}: View Count
- {%8}: Description

With this, we can move on to defining the items.

#### Defining the Items

In this step we use the numbered placeholders we found above to define our items. When the generator sees the numbered placeholders it will replace it with the correct data for that item, so {%2} will be replaced with "Sooubway 4: The Final Sandwich" for item 1, "Last To Take Hand Off Boat, Keeps It" for item 2 and so on.

So when defining our item, the item title will be {%2}.

<p>Likewise, the link will be "https://youtube.com/watch?v={%1}".</p>

For the description, we'll include some simple HTML formatting. We'll have the video's title and duration on one line followed by the Channel name, view count and upload time on the next, and the video description last. 

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/item.jpg">
</p>

Any HTML in the description needs to be within the <!CDATA\[ tags. CSS can be inlined, but most readers will drop any <style> or <script> tags. 
  
If you don't want to use HTML in the description, you can simply delete the <!CDATA\[ tags, or ignore them.

The GUID field is an ID used by feed readers to determine if an item is new to a feed. In our case, {%1} is the youtube video ID, so we can use that.

When you are done, simply click the "Submit" button, and you should be taken to a page that looks like this:

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/success.jpg">
</p>

<p align="center">
  <strong>Congratulations! You've made your first custom feed!</strong>
  </br>
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Bocchi.png" width=500 height=500>
</p>

*****

### Adding a Feed to Your Feed Reader


1.	Go to "My Feeds"
2.	Click on the feed you want to add
3.	You should see a Feed Details & Preview page like the one on the below

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/preview.jpg">
</p>

4.	Copy this page's URL (Should be something like Localhost:8000/Feeds/Feed_Name.xml)
5.	Paste the URL into wherever your feed reader asks for the Feed URL

<p align="center">
  <img src="https://github.com/k-barber/RSS-Generator/blob/master/Img/Readme%20images/save.jpg">
</p>

*****

### Deleting a Feed

Currently the only way to delete a feed is remove the feed from the Feed_Definitions.txt file and delete the feed's .xml file in the Feeds folder.

*****

## Compatible Feed Readers


<table>
  <tr>
    <th>
      Compatible
    </th>
    <th>
      Incompatible
    </th>
  </tr>
  <tr>
    <td>
      <a href="https://nodetics.com/feedbro/">Feedbro</a></br>
      <a href="https://quiterss.org/">QuiteRSS</a></br>
      <a href=""></a></br>
    </td>
    <td>
      <a href="https://feedly.com/">Feedly</a></br>
      <a href=""></a></br>
    </td>
  </tr>
</table>

*****

## Support the Developer
