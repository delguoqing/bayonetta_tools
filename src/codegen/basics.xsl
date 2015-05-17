<?xml version="1.0"?>

<!DOCTYPE stylesheet[
<!ENTITY space "<xsl:text> </xsl:text>">
<!ENTITY cr "<xsl:text>
</xsl:text>">
<!ENTITY sep "<xsl:text/>">
<!ENTITY e2 "<xsl:text>
		</xsl:text>">
]>

<xsl:stylesheet	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:exsl="http://exslt.org/common"
		extension-element-prefixes="exsl"
		version="1.0">
	
<!-- declare -->
<xsl:template match="jump_to" mode="declare_and_load">
&sep;f.seek(<xsl:value-of select="@offset"/>, 0)&sep;
</xsl:template>
<xsl:template match="skip" mode="declare_and_load">
&sep;f.seek(<xsl:value-of select="@size"/>, 1)&sep;
</xsl:template>
<xsl:template match="*[@dummy_value]" mode="declare_and_load">
&sep;self.<xsl:value-of select="@name"/> = <xsl:value-of select="@dummy_value"/>
</xsl:template>
<xsl:template match="require" mode="declare_and_load">
&sep;self.<xsl:value-of select="@name"/> = <xsl:value-of select="@name"/>		
</xsl:template>
<xsl:template match="*" mode="declare_and_load">
&sep;self.<xsl:value-of select="@name"/> = <xsl:apply-templates select="." mode="load_from_file"/>&sep;
	<xsl:if test="@assert_value='1'">
&sep;;assert self.<xsl:value-of select="@name"/> == <xsl:apply-templates select="." mode="value"/>,&sep;
&sep;"value assert fail for '<xsl:value-of select="@name"/>': expect <xsl:apply-templates select="." mode="value"/>, get %r" % self.<xsl:value-of select="@name"/>
	</xsl:if>
	<xsl:if test="@value_statistic='1'">
&sep;;add_value_statistic("<xsl:value-of select="@name"/>", self.<xsl:value-of select="@name"/>)&sep;
	</xsl:if>	
</xsl:template>

<!-- load from file -->
<xsl:template name="numeric_type" match="uint8|int8|uint16|int16|uint32|int32|float" mode="load_from_file">
<xsl:if test="@fix_value">
	&sep;(&sep;
</xsl:if>	
&sep;struct.unpack("&sep;
	<xsl:apply-templates select="." mode="struct"/>", &sep;
	&sep;f.read(<xsl:apply-templates select="." mode="size"/>))[0]&sep;
<xsl:if test="@fix_value">
	&sep; + (<xsl:value-of select="@fix_value"/>))&sep;
</xsl:if>	
</xsl:template>

<xsl:template match="fixed16" mode="load_from_file">
	&sep;((<xsl:call-template name="numeric_type" select="." mode="struct"/>)*1.0/(1&lt;&lt;<xsl:value-of select="@shift"/>))&sep;
</xsl:template>

<xsl:template match="bool" mode="load_from_file">
&sep;bool(<xsl:call-template name="numeric_type" select="." mode="struct"/>)&sep;
</xsl:template>

<xsl:template match="string" mode="load_from_file">
	<xsl:call-template name="numeric_type" select="." mode="struct"/>.rstrip("\x00")&sep;
</xsl:template>

<xsl:template match="list" mode="load_from_file">
&sep;[&sep;
	<xsl:apply-templates select="./*" mode="load_from_file"/>
	&sep; for _ in xrange(<xsl:value-of select="@size"/>)&sep;
&sep;]</xsl:template>

<xsl:template match="type" mode="load_from_file">
&sep;cls_<xsl:value-of select="@typename"/>(f)&sep;
</xsl:template>

<!-- value -->
<xsl:template match="int8|uint8|int16|uint16|int32|uint32|float|string|fixed16" mode="value"><xsl:value-of select="@value"/></xsl:template>
<xsl:template match="string" mode="value">'<xsl:value-of select="@value"/>'</xsl:template>
<xsl:template match="unicode" mode="value">u'<xsl:value-of select="@value"/>'</xsl:template>

<!-- size -->
<xsl:template match="*[@dummy_value]|require" mode="size">0</xsl:template>
<xsl:template match="uint8|int8|bool" mode="size">1</xsl:template>
<xsl:template match="uint16|int16|fixed16" mode="size">2</xsl:template>
<xsl:template match="uint32|int32|float" mode="size">4</xsl:template>
<xsl:template match="string" mode="size"><xsl:value-of select="@size"/></xsl:template>
<xsl:template match="type" mode="size">
&sep;cls_<xsl:value-of select="@typename"/>.get_unit_size()&sep;
</xsl:template>
<xsl:template match="list" mode="size">
<xsl:value-of select="@size"/> * <xsl:apply-templates select="./*" mode="size"/>
</xsl:template>

<!-- struct format -->
<xsl:template name="endian">
	<xsl:choose>
		<xsl:when test="@endian">
			<xsl:choose>
				<xsl:when test="starts-with(@endian, 'LE')">&lt;</xsl:when>
				<xsl:otherwise>&gt;</xsl:otherwise>
			</xsl:choose>
		</xsl:when>
		<xsl:otherwise>
			<xsl:choose>
				<xsl:when test="/format[starts-with(@endian, 'LE')]">&lt;</xsl:when>
				<xsl:otherwise>&gt;</xsl:otherwise>
			</xsl:choose>			
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="int8" mode="struct">
	<xsl:call-template name="endian"/>b</xsl:template>
<xsl:template match="uint8|bool" mode="struct">
	<xsl:call-template name="endian"/>B</xsl:template>
<xsl:template match="int16|fixed16" mode="struct">
	<xsl:call-template name="endian"/>h</xsl:template>
<xsl:template match="uint16" mode="struct">
	<xsl:call-template name="endian"/>H</xsl:template>
<xsl:template match="int32" mode="struct">
	<xsl:call-template name="endian"/>i</xsl:template>
<xsl:template match="uint32" mode="struct">
	<xsl:call-template name="endian"/>I</xsl:template>
<xsl:template match="float" mode="struct">
	<xsl:call-template name="endian"/>f</xsl:template>
<xsl:template match="string" mode="struct">
	<xsl:apply-templates select="." mode="size"/>s&sep;
</xsl:template>

<!-- default value -->
<xsl:template match="uint8|int8|uint16|int16|uint32|int32">0</xsl:template>
<xsl:template match="bool">False</xsl:template>
<xsl:template match="float|fixed16">0.0</xsl:template>
<xsl:template match="null">None</xsl:template>
<xsl:template match="string">""</xsl:template>
<xsl:template match="list">[]</xsl:template>

<!-- align -->
<xsl:template name="align">
&sep;f.seek((f.tell() + (<xsl:value-of select="@align_offset"/>) + <xsl:value-of select="@align"/> - 1) // <xsl:value-of select="@align"/> * <xsl:value-of select="@align"/> - (<xsl:value-of select="@align_offset"/>))&sep;
</xsl:template>

<!-- import base class module -->
<xsl:template name="import_base_module">
<xsl:if test="@base_module='1'">
&sep;import ex_<xsl:value-of select="@typename"/>&sep;
</xsl:if>
</xsl:template>

<!-- base class -->
<xsl:template name="base_test">
<xsl:value-of select="name()"/>
</xsl:template>

<xsl:template name="base">
<xsl:choose>
<xsl:when test="@base_module='1'">
	&sep;ex_<xsl:value-of select="@typename"/>.cls_obj&sep;
</xsl:when>
<xsl:otherwise>
	&sep;object&sep;
</xsl:otherwise>
</xsl:choose>
</xsl:template>

<!-- required arg -->
<xsl:template name="unpack_args">
	<xsl:for-each select="./require">
		&sep;, <xsl:value-of select="@name"/>
	</xsl:for-each>
</xsl:template>
<xsl:template name="pack_args">
	<xsl:value-of select="name()"/>
	<xsl:for-each select="./*">
		&sep;, self.<xsl:value-of select="@name"/>
	</xsl:for-each>
</xsl:template>

</xsl:stylesheet>