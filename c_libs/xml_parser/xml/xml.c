#include "SKcommon.h"
#include "xml.h"
#include "expat.h"
#include "string.h"

#define BUFFSIZE 8192
static char _XMLBuffer[BUFFSIZE];


static void _Printinfo_element_handle_start(void *userData, const char *name, const char **attr)
{
	int i;
	int *depthPtr = (int *)userData;
	for (i = 0; i < *depthPtr; i++)
	{
		printf("  ");
	}
	printf("%s",name);

	for (i = 0; attr[i]; i+=2)
	{
		printf(" %s='%s'", attr[i], attr[i+1]);
	}
	
	printf("\n");

	*depthPtr +=1;
}

static void _Printinfo_element_handle_end(void *userData, const char *name)
{
	int i = 0;
	int *depthPtr = (int *)userData;
	
	*depthPtr -=1;	

	for (i = 0; i < *depthPtr; i++)
	{
		printf("  ");
	}
	printf("%s\n",name);
}

static void _Printinfo_char_handle(void *userData, const XML_Char *s, int len)
{
	int i = 0;
	int *depthPtr = (int *)userData;
	char temp[80];
	
	memset(temp,'\0',80);

	if (len <= 1)
	{
		/*do nothing with length is 1*/
		return;
	}

	for (i = 0; i < *depthPtr-1; i++)
    {
        printf("  ");
    }
	
	if(len < 80)
	{
		memcpy(temp,s,len);
	}
	else
	{
		memcpy(temp,s,80);
	}

	printf("%s\n",temp);
}

bool SKApi_XML_Printinfo(FILE *xmlfile)
{
	int done = 0;
	int depth = 0;
	int len = 0;
	XML_Parser parser = XML_ParserCreate(NULL);

	if (!parser)
	{
		printf("Couldn't allocate memory for parser \n");
		return false;
	}

	XML_SetUserData(parser, &depth);
	XML_SetElementHandler(parser, _Printinfo_element_handle_start, _Printinfo_element_handle_end);
	XML_SetCharacterDataHandler(parser,_Printinfo_char_handle);

	do
	{
		len = (int)fread(_XMLBuffer, 1, sizeof(_XMLBuffer), xmlfile);
		if (ferror(xmlfile))
		{
			printf("Read xmlfile error\n");
			return false;
		}		
		
		done = feof(xmlfile);
		
		if(XML_Parse(parser, _XMLBuffer, len, done) == XML_STATUS_ERROR)
		{
			printf("Parse error at line %ld:\t%s\n", 
					XML_GetCurrentLineNumber(parser),
					XML_ErrorString(XML_GetErrorCode(parser)));
			return false;
		}	
	}while(!done);
	
	XML_ParserFree(parser);
	return true;
}

bool SKApi_XML_Help(void)
{
	printf("=============XML Commnd List==================\n");
	printf("[1] print xml information\n");
	printf("     XML_Parser 1 example/example1.xml\n");
	printf("[2] continue ...\n");
	printf("==============================================\n");

	return true;
}
