from secrets import token_urlsafe

import typer

app = typer.Typer()


@app.command()
def main(
        length: int = typer.Option(16, "-l", "--length", help="Token's length")
):
    token = token_urlsafe(length)
    typer.echo(token)


if __name__ == '__main__':
    app()
