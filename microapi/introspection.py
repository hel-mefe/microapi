from microapi.core.router import BaseRouter


def render_endpoints_page(router: BaseRouter) -> str:
    rows = []

    for method, path, handler in router.routes():
        rows.append(
            f"""
            <tr>
                <td>{method}</td>
                <td>{path}</td>
                <td>{handler.__name__}</td>
            </tr>
            """
        )

    rows_html = "\n".join(rows)

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>MicroAPI Endpoints</title>
            <style>
                body {{
                    font-family: monospace;
                    background: #0b0b0b;
                    color: #e5e5e5;
                    margin: 0;
                }}
                header {{
                    display: flex;
                    align-items: center;
                    padding: 16px 24px;
                    border-bottom: 1px solid #222;
                }}
                header img {{
                    height: 28px;
                }}
                main {{
                    padding: 24px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    padding: 8px 12px;
                    border-bottom: 1px solid #222;
                }}
                th {{
                    text-align: left;
                    color: #6ee7b7;
                }}
                tr:hover {{
                    background: #111;
                }}
            </style>
        </head>
        <body>
            <header>
                <img src="assets/microapi.png" width="200px" height="64px" alt="MicroAPI logo" />
            </header>
            <main>
                <h1>Registered Endpoints</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Method</th>
                            <th>Path</th>
                            <th>Handler</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </main>
        </body>
    </html>
    """
