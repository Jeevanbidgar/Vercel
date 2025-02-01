import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  # OK
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS for all origins
        self.end_headers()

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        names = query_params.get('name', [])  # Get a list of names

        try:
            with open('q-vercel-python.json', 'r') as f:
                student_data = json.load(f)

            marks = []
            for name in names:
                mark = student_data.get(name)
                if mark is not None:
                    marks.append(mark)
                else:
                    marks.append(0) # Or handle the case where the name isn't found

            response_data = {"marks": marks}
            self.wfile.write(json.dumps(response_data).encode())

        except FileNotFoundError:
            self.send_error(404, "Data file not found")
        except json.JSONDecodeError:
            self.send_error(500, "Invalid JSON data")
        except Exception as e:
            self.send_error(500, f"An error occurred: {e}")


def main():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, handler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
