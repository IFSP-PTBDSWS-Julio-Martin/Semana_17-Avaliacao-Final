# A very simple Flask Hello World app for you to get started with...
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class LoginForm(FlaskForm):
    nome = StringField('Cadastre o novo Aluno:', validators=[DataRequired()])
    disciplina = SelectField('Disciplina associada:',
                             choices=[
                                 ('DSWA5', 'DSWA5'),
                                 ('GPSA5', 'GPSA5'),
                                 ('IHCA5', 'IHCA5'),
                                 ('SODA5', 'SODA5'),
                                 ('PJIA5', 'PJIA5'),
                                 ('TCOA5', 'TCOA5')
                             ])
    submit = SubmitField('Cadastrar')

class Alunos(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'))

    def __repr__(self):
        return f'<Aluno {self.nome}>'

class Disciplinas(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True)
    alunos = db.relationship('Alunos', backref='disciplina', lazy='dynamic')

    def __repr__(self):
        return f'<Disciplina {self.nome}>'

@app.route('/')
def index():
    current_time = datetime.utcnow()
    return render_template(
        'index.html',
        current_time=current_time
    )

@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    form = LoginForm()

    if form.validate_on_submit():
        nome = form.nome.data
        disc = form.disciplina.data

        disciplina = Disciplinas.query.filter_by(nome=disc).first()

        if disciplina is None:
            disciplina = Disciplinas(nome=disc)
            db.session.add(disciplina)
            db.session.commit()

        aluno = Alunos(nome=nome, disciplina=disciplina)
        db.session.add(aluno)
        db.session.commit()

        flash("Aluno cadastrado com sucesso!")
        return redirect(url_for('alunos'))

    lista = Alunos.query.all()

    return render_template('alunos.html', form=form, lista=lista)

@app.route('/ocorrencias')
def ocorrencia():
    current_time = datetime.utcnow()
    return render_template('ocorrencias.html', current_time=current_time)

if __name__ == "__main__":
    app.run(debug=True)
