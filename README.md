# WebText micro-service
## RESTFUL API
## Parse and convert content from web page


### File structure
| Path                                                                   | Description                         |
|------------------------------------------------------------------------|-------------------------------------|
| [main.py](main.py)                                                     | Flask entry point                   |
| [application/](application/__init__.py)                                | Flask application and sub apps init |
| [docker/workspace/requirements.txt](docker/workspace/requirements.txt) | Application requirements            |
| [configs/](configs/__init__.py)                                        | All application configs             |
| [src/modules/](src/modules/)                                           | Entry point for sub apps            |
| [src/modules/api_v1/](src/modules/api_v1/__init__.py)                  | Init sub app: restful api           |
| [src/helpers.py](src/helpers.py)                                       | Some additional functions           |
| [src/class_result.py](src/class_result.py)                             | Class for creating result           |
| [src/convertor/](src/convertor/_convertor.py)                          | Converting content from xml to md   |
| [src/parser/](src/parser/_parser.py)                                   | Parsing web page. Getting html      |


### Installation
```bash
cd docker
cp .env.example .env
docker-compose -p webtext up -d --build
```

## API URLS:

#### **POST: /api/v1/collect**

#### Parse web page and return content in md format

#### **Parameters**
| Parameter name     | Description                         | Type | Default value | Required |
|--------------------|-------------------------------------|------|---------------|----------|
| url                | url for web page                    | str  | -             | yes      |
| timeout            | tiemout for requests                | int  | 15            | no       | 
| proxy              | proxy for requests                  | json | -             | no       | 
| with_metadata      | extract metadata                    | bool | False         | no       | 
| auto_convert_to_md | after parsing convert content to md | bool | True          | no       |
| method_parse       | parse web page selenium or request  | str  | request       | no       |


### Usage example:

**With another proxy:**

```bash
curl -H "Content-Type: application/json" -d '{
    "url": "https://thebestordernow.com/persuasive-essay-topics-with-3-points",
    "proxy": {
    	"host": "127.0.0.1",
    	"port": "8080",
    	"username": "dima",
    	"password": "hanza"
    }
}' -X POST http://localhost:5004/api/v1/collect
```

**With default proxy from config:**

```bash
curl -H "Content-Type: application/json" -d '{
    "url": "https://thebestordernow.com/persuasive-essay-topics-with-3-points",
    "proxy": "default"
}' -X POST http://localhost:5004/api/v1/collect
```

**Parsing through proxy with selenium:**

```bash
curl -H "Content-Type: application/json" -d '{
    "url": "https://thebestordernow.com/persuasive-essay-topics-with-3-points",
    "method_parse": "selenium",
    "proxy": {
    	"host": "127.0.0.1",
    	"port": "8080",
    	"username": "dima",
    	"password": "hanza"
    }
}' -X POST http://localhost:5004/api/v1/collect
```

#### **POST: /api/v1/convert**

#### Converting html text to md

#### **Parameters**

| Parameter name | Description  | Type | Default value | Required |
|----------------|--------------|------|---------------|----------|
| source         | type of text | str  | html          | no       |
| text           | html text    | int  | 15            | yes      | 



### Usage example:

**Convert**

```bash
curl -H "Content-Type: application/json" -d '{
    "source": "HTML",
    "text": "<h2>header</h2><p>Some text</p>"
    }
}' -X POST http://localhost:5004/api/v1/convert
```


### Answer:

```json
{
	"status": "success",
	"result": "data result"
}
```

### Error:
```json
{
	"status": "error",
	"message": "message with error"
}
```