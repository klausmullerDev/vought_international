from app import create_app, db

# Inicialize o aplicativo Flask
app = create_app()

# Use o contexto do aplicativo para criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
