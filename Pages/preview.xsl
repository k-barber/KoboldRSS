<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 
<xsl:template match="/rss/channel">
  <html>
    <head>
        <link rel="stylesheet" href="/Pages/styles.css"></link>
        <title>RSS-Manager:<xsl:value-of select="title"/></title>
    </head>
    <body>
        <a href="/"><img src="/Bocchi.png" id="bocchi"/></a>
        <div id="container">
            <div>
                <a href="https://validator.w3.org/feed/docs/rss2.html" target="_blank"><img id="icon" src="/RSS.png"/></a>
                <p><a href="/">Home</a> &gt; <a href="/Feeds/">Feeds</a> &gt; <xsl:value-of select="title"/>.xml</p>
                <h1>K-Barber's RSS-Manager: Feed Details &amp; Preview</h1>
                <p>Congratulations! If you can see this page, you are ready to add your custom feed to your feed reader!</p>
                <p>Simply add this page's url into your feed reader and you're all done.</p>
                <hr/>
                <h3>Feed Name: <xsl:value-of select="title"/></h3>
                <xsl:variable name="feedlink"><xsl:value-of select="link" /></xsl:variable>
                <h3>Feed Link: <a href="{$feedlink}"><xsl:value-of select="link"/></a></h3>
                <h3>Feed Description: <xsl:value-of select="description"/></h3>
                <h3>Feed Language: <xsl:value-of select="language"/></h3>
                <h3>Feed TTL: <xsl:value-of select="ttl"/></h3>
                <h3>Feed Content: </h3>
                <br/>
                <table>
                    <tr>
                    <th>Title</th>
                    <th>GUID</th>
                    <th>Link</th>
                    <th>Description</th>
                    </tr>
                    <xsl:for-each select="item">
                        <tr>
                            <td><p><xsl:value-of select="title"/></p></td>
                            <td><xsl:value-of select="guid"/></td>
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
            console.log(descriptions);
            [].forEach.call(descriptions, function(description){
                inner = description.innerHTML;
                inner = inner.replace(/&lt;/g, "<");
                inner = inner.replace(/&gt;/g, ">");
                inner = inner.replace(/&amp;/g, "&");
                console.log(inner);
                description.innerHTML = inner;
            });
            ]]>
        </script>
    </body>
  </html>
</xsl:template>
 
</xsl:stylesheet>