
#include "SKcommon.h"
#include "xml.h"

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
		printf("XML_Parser [Command] [XML file]\n");
		SKApi_XML_Help();
		return 0;
    }
	
	int _intXMLcommnad = atoi(argv[1]);
    FILE *_pfXMLinputfile = NULL;
    bool _bXMLret = false;


	_pfXMLinputfile = fopen(argv[2],"r");
	if (_pfXMLinputfile == NULL)
	{
		printf("open file error: %s\n",argv[2]);
		return 0;
	}

	printf("parsing file : %s \n",argv[2]);
	
	switch (_intXMLcommnad)
	{
		default:
		case 1: /*print XML file info*/
			_bXMLret = SKApi_XML_Printinfo(_pfXMLinputfile);
			break;
	}	

	fclose(_pfXMLinputfile);
    
    if (!_bXMLret)
    {
        printf("failed\n");
    }

    return 1;
}
