<h1 style="text-align: center;">Тестовое задание</h1>
<p>При выполнении задания были использованы:</p>
<p>-Django/DRF</p>
<p>-Postgresql</p>
<p>Хочу сразу отметить, что сборка докера оказалось самой тяжелой задачей, хотя казалось бы, должно быть это наоборот. Случилось это, так как на моем текущем компьютере(windows 7) не поддерживается докер. Поднять в виртуальной машине тоже не вышло, так как виртуализация тоже не работает. Но не смотря на это я все равно составил логику развертывания докер контейнеров.</p>
<h1 style="text-align: center;">Инициализация</h1>
<p>Самый смутный момент это импорт csv в базу данных, по условиям задачи путь задается в enviroment, но дело в том, что в таких условиях эту переменную среды будет видеть только докер контейнер без доступа к хост машине. Этого бы можно было избежать если бы csv файл просто бы копировался в контейнер при инициализации. Но в данный момент проект предполагает наличие csv в контейнере и вытащит путь к нему из ENV</p>
<p>При развертывании проекта точка входа в докер контейнере запускает bash скрипт, кторый</p>
<p>-инициализирует базу данных</p>
<p>-импортирует в нее CSV файл взятый из . env окружения</p>
<p>- создает задачу для crontab выгружать логи пользовательской командой для django каждые полчаса</p>
<p>-запускает сервер</p>
<p>&nbsp;</p>
<p align="center">&nbsp;</p>
<h1 style="text-align: center;">Структура БД</h1>
<p>БД состоит из 3 таблиц:</p>
<p>1) основная (хранение станций)</p>
<p>2) промежуточная для сбора логов(тут собираются все запросы через миддлварь, которые можно анализировать через админку)</p>
<p>3) конечная, приведенная к стандарту&nbsp;</p>
<table border="1" cellpadding="1" cellspacing="1" style="width: 500px">
	<tbody>
		<tr>
			<td>id</td>
			<td>log(JsonField)</td>
		</tr>
		<tr>
			<td>1</td>
			<td>{&quot;service&quot;: &quot;metro&quot;, &quot;message&quot;: 200, &quot;error&quot;: null, &quot;endpoint&quot;: &quot;/api/data/list/2/5?format=json&quot;}</td>
		</tr>
	</tbody>
</table>
<p>Данные из промежуточной таблицы переносятся в конечную каждые 30 минут. Интуитивно понятно, что это не лучшее решение, но я не особо силен в логгировании и это единственная задумка, которую получилось реализовать</p>
<p>Так как нужно было на что то опираться, то приложение писалось для Московского метрополитена (максимальный размер текстовых ячеек соответствует самым длинным словам)</p>
<h1 style="text-align: center;">API</h1>
<p>1) GET /api/data/{id}&nbsp;</p>
<table border="1" cellpadding="1" cellspacing="1" style="width: 500px">
	<tbody>
		<tr>
			<td>id</td>
			<td>int</td>
		</tr>
	</tbody>
</table>
<p>возвращает одну запись, если запись не найдена, то генерирует ошибку 404</p>
<p>2)&nbsp;GET /api/data/list/{page}/{limit}</p>
<table border="1" cellpadding="1" cellspacing="1" style="width: 500px">
	<tbody>
		<tr>
			<td>page</td>
			<td>int</td>
		</tr>
		<tr>
			<td>limit</td>
			<td>int</td>
		</tr>
	</tbody>
</table>
<p>Пагинация устроена таким образом, что на одной странице - 20 записей, если лимит превышает число записей на странице, то генерируется ошибка</p>
<p>нумерация page начинается с 1</p>
<p>Возвращает отсортированный список объектов&nbsp;</p>
<p>3)POST /api/data/add</p>
<p>json in body:</p>
<div>{</div>
<div>&quot;station&quot;: &quot;&quot;,</div>
<div>&nbsp;&quot;line&quot;: &quot;&quot;,</div>
<div>&nbsp;&quot;admarea&quot;: &quot;&quot;,</div>
<div>&nbsp;&quot;district&quot;: &quot;&quot;,</div>
<div>&nbsp;&quot;status&quot;: &quot;&quot;,</div>
<div>&nbsp;&quot;ID&quot;:</div>
<div>}</div>
<table border="1" cellpadding="1" cellspacing="1" style="width: 500px">
	<tbody>
		<tr>
			<td>station</td>
			<td>str | required</td>
		</tr>
		<tr>
			<td>line</td>
			<td>str | required</td>
		</tr>
		<tr>
			<td>admarea</td>
			<td>str | required</td>
		</tr>
		<tr>
			<td>district</td>
			<td>str | required</td>
		</tr>
		<tr>
			<td>status</td>
			<td>str | required</td>
		</tr>
		<tr>
			<td>ID</td>
			<td>null or int | optional</td>
		</tr>
	</tbody>
</table>
<p>4)&nbsp;DELETE /api/data/{id}</p>
<p>Удаляет 1 запись, при успехе возвращает код 200, если запись не существует, то генерируется код 404</p>
<table border="1" cellpadding="1" cellspacing="1" style="width: 500px">
	<tbody>
		<tr>
			<td>id</td>
			<td>int</td>
		</tr>
	</tbody>
</table>
<p>5) GET /api/data/search</p>
<p>принимает URL параметры для поиска</p>
<p>search - то, что ищем&nbsp;</p>
<p>search_fields - в каких полях</p>
<p>Пример:</p>
<p>&nbsp;/api/data/search?search=Ленина&amp;search_fields=line&amp;search_fields=station</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
