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
                <h1>K-Barber's RSS-Manager: <xsl:value-of select="title"/></h1>
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
                            <td><xsl:value-of select="description"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </div>
        </div>
    </body>
  </html>
</xsl:template>
 
</xsl:stylesheet>