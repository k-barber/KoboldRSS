<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 
<xsl:template match="/rss/channel">
  <html>
    <head>
        <link rel="stylesheet" href="/css/styles.css"></link>
        <title>KoboldRSS: <xsl:value-of select="title"/></title>
    </head>
    <body>
        <a href="/"><img src="/img/Logo_V.0.4.png" id="floating_logo" /></a>
        <div id="container">
            <div>
                <a href="https://www.rssboard.org/rss-specification" target="_blank"><img id="icon" src="/img/RSS.png"/></a>
                <p id="bread-crumbs"><a href="/">Home</a> &gt; <a href="/Feeds/">My Feeds</a> &gt; <xsl:value-of select="title"/>.xml</p>
                <h1 style="display: flex; align-items: center;">
                    <a href="/" style="margin-right: 15px;"><img height="55px" src="/img/Logo_Large_shadow.png"></img></a>Feed Details &amp; Preview
                </h1>
                <p>Congratulations! If you can see this page, you are ready to add your custom feed to your feed reader!</p>
                <p>Simply copy and paste this page's url into your feed reader and you're all done.</p>
                <hr/>
                <p>Feed Name: <xsl:value-of select="title"/></p>
                <xsl:variable name="feedlink"><xsl:value-of select="link" /></xsl:variable>
                <xsl:variable name="doclink"><xsl:value-of select="docs" /></xsl:variable>
                <xsl:variable name="generatorlink"><xsl:value-of select="generator" /></xsl:variable>
                <p>Feed Link: <a href="{$feedlink}"><xsl:value-of select="link"/></a></p>
                <p>Feed Description: <xsl:value-of select="description"/></p>
                <p>Feed Language: <xsl:value-of select="language"/></p>
                <p>Feed Last Build Date: <xsl:value-of select="lastBuildDate"/></p>
                <p>Feed TTL: <xsl:value-of select="ttl"/></p>
                <p>Feed Content: </p>
                <br/>
                <table>
                    <tr>
                    <th id="title-header">Title</th>
                    <th>Link</th>
                    <th id="description-header">Description</th>
                    </tr>
                    <xsl:for-each select="item">
                        <tr>
                            <td><p><xsl:value-of select="title"/></p></td>
                            <xsl:variable name="hyperlink"><xsl:value-of select="link" /></xsl:variable>
                            <td><a href="{$hyperlink}"><xsl:value-of select="link"/></a></td>
                            <td><p class="description"><xsl:value-of select="description"/></p></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </div>
        </div>
        <script>
        <![CDATA[
            var descriptions = document.getElementsByClassName("description");
            [].forEach.call(descriptions, function(description){
                inner = description.innerHTML;
                inner = inner.replace(/&lt;/g, "<");
                inner = inner.replace(/&gt;/g, ">");
                inner = inner.replace(/&amp;/g, "&");
                description.innerHTML = inner;
            });
            ]]>
        </script>
        <script>
        <![CDATA[
            var bread = document.getElementById("bread-crumbs");
            var pieces = location.pathname.split("/");
            for (index = pieces.length - 1; index > 2; index--) {
                var href = pieces.slice(0, index).join("/");
                console.log(href)
                var link = document.createElement("a");
                link.href = href
                console.log(link)
                link.appendChild(document.createTextNode(pieces[index - 1]));
                bread.childNodes[2].after(link)
                bread.childNodes[2].after(document.createTextNode(" > "))
            }
        ]]>
        </script>
    </body>
  </html>
</xsl:template>
 
</xsl:stylesheet>