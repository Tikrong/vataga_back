from vataga_games_catalogue import app, logger, db, sql_engine
from sqlalchemy.orm import Session


class Game(db.Model):
    """Модель для хранения данных об играх"""

    __tablename__ = 'games'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode)
    minPlayers = db.Column(db.Integer)
    maxPlayers = db.Column(db.Integer)
    minTime = db.Column(db.Integer)
    maxTime = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    description = db.Column(db.Text(65000))

    @staticmethod
    def add_games(games: list[dict]) -> int:
        """метод для добавления в базу новых игр из полученного списка коллекций"""
        with Session(sql_engine) as session:
            counter = 0
            for game in games:
                try:
                    game_entry = Game(title=game['title'], minPlayers=game['minPlayer'], maxPlayers=game['maxPlayers'],
                                 minTime=game['minTime'], maxTime=game['maxTime'], difficulty=game['difficulty'],
                                 description=game['description'])
                    session.add(game_entry)

                    for img in game['src']:
                        print(game_entry.id)
                        img_entry = Image(gameId=game_entry.id, src=img.split("/")[1])
                        session.add(img_entry)

                    counter += 1

                except Exception as e:
                    logger.error(f"Couldn't add {game} to session, got error {e}")

            try:
                session.commit()
                return counter

            except Exception as e:
                logger.error(f"Couldn't commit games to db, got error {e}")

    @staticmethod
    def get_games():
        """метод для получения списка игр из базы данных"""
        with Session(sql_engine) as session:

            images = {}
            results = session.query(Image).all()
            for result in results:
                if result.gameId in images:
                    images[result.gameId].append(result.src)
                else:
                    images[result.gameId] = [result.src]

            results = session.query(Game).all()
            games = []
            for result in results:
                game = {'id': result.id,
                    'title': result.title,
                    'minPlayers': result.minPlayers,
                    'maxPlayers': result.maxPlayers,
                    'minTime': result.minTime,
                    'maxTime': result.maxTime,
                    'difficulty': result.difficulty,
                    'description': result.description,
                    'src': images[result.id]}
                games.append(game)

            return games


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    gameId = db.Column(db.Integer)
    src = db.Column(db.Unicode)
