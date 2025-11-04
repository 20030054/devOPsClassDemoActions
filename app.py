from flask import Flask, render_template_string, request, session, make_response
import random
import uuid 

# --- Flask Configuration ---
app = Flask(__name__)
# IMPORTANT: Use a complex, randomly generated key in a real application
app.secret_key = 'supersecretkey123_updated_and_more_secure_for_session' 

# --- Data ---
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why did the teddy bear say no to dessert? Because she was stuffed.",
    "Why did the soccer player take so long to eat dinner? Because he thought he couldn't use his hands.",
    "Name the kind of tree you can hold in your hand? A palm tree!",
    "What do birds give out on Halloween? Tweets.",
    "What has ears but cannot hear? A cornfield.",
    "What's a cat's favorite dessert? A bowl full of mice-cream.",
    "Where did the music teacher leave her keys? In the piano!",
    "What did the policeman say to his hungry stomach? “Freeze. You're under a vest.”",
    "What did the left eye say to the right eye? Between us, something smells!",
    "What do you call a guy who's really loud? Mike.",
    "Why do birds fly south in the winter? It's faster than walking!",
    "What did the lava say to his girlfriend? “I lava you!”",
    "Why did the student eat his homework? Because the teacher told him it was a piece of cake.",
    "What did Yoda say when he saw himself in 4k? HDMI.",
    "Which superhero hits home runs? Batman!",
    "What's Thanos' favorite app on his phone? Snapchat.",
    "Sandy's mum has four kids; North, West, East. What is the name of the fourth child? Sandy, obviously!",
    "What is a room with no walls? A mushroom.",
    "Why did the blue jay get in trouble at school? For tweeting on a test!",
    "What social events do spiders love to attend? Webbings.",
    "What did one pickle say to the other? Dill with it.",
    "What do you call fake spaghetti? An impasta!",
    "Why was the computer cold? It left its Windows open!",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "The problem with candy jokes is they're either too sweet or too corny.",
    "What did the ocean say to the beach? Nothing, it just waved.",
    "How does a penguin build its house? Igloos it together?",
    "I'm on a whiskey diet. I've lost three days already.",
    "Knock, knock. Who's there? Lettuce. Lettuce who? Lettuce in, it's freezing out here!",
    "Knock, knock. Who's there? Ya. Ya who? No thanks, I prefer Google.",
    "Knock, knock. Who's there? Broken pencil. Broken pencil who? Forget it. It's pointless.",
    "What happens if you don't pay your exorcist? You get repossessed!",
    "I'm on a seafood diet. I see food, and I eat it.",
    "I'm writing a book on reverse psychology. Don't buy it.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "I have a fear of speed bumps, but I am slowly getting over it.",
    "I'm no good at math, but I know that 5 out of 4 people struggle with it.",
    "Why do bananas never feel lonely? Because they all hang out in bunches.",
    "I was addicted to the hokey pokey, but then I turned myself around.",
    "What's a skeleton's least favorite room? The living room.",
    "I just burned 1200 calories. I forgot the pizza in the oven.",
    "What's the hardest tea to swallow? Reality.",
    "I was raised as an only child. It drove my sister nuts.",
    "What kind of shoes do frogs wear? Open-toad sandals.",
    "I just built an ATM that only gives out coins. It's an automatic coin machine.",
    "What happened when two slices of bread went on a date? It was loaf at first sight.",
    "Why do crabs never volunteer? Because they're shell-fish.",
    "I had a quiet game of tennis today. There was no racket.",
]

colors = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#6f42c1', '#17a2b8', '#fd7e14', '#e83e8c', '#6610f2']

facts = [
    "A single cloud can weigh more than 1 million pounds.",
    "The world's largest living organism is a fungus, spanning over 2,200 acres in Oregon.",
    "There are more trees on Earth than stars in the Milky Way galaxy.",
    "A day on Venus is longer than a year on Venus.",
    "Hot water freezes faster than cold water. This is called the Mpemba effect.",
    "The shortest war in history lasted only 38 to 45 minutes (between Britain and Zanzibar in 1896).",
    "Octopuses have three hearts: two pump blood through the gills and one circulates blood to the rest of the body.",
    "Bananas are berries, but strawberries are not.",
    "Animals that lay eggs don't have belly buttons.",
    "Mr. Potato Head was the first toy to be advertised on TV.",
    "Boanthropy is a psychological disorder in which patients believe they are a cow.",
    "Camels have three eyelids.",
    "There is a McDonald's on every continent except Antarctica.",
    "Mosquitoes are attracted to people who just ate bananas.",
    "Cats can make more than 100 vocalizations.",
    "The world's termites outweigh the world's humans by about 10 to 1.",
    "Most toilet paper sold in France is pink.",
    "The Hawaiian alphabet only has 12 letters.",
    "The human nose can remember 50,000 different scents.",
    "Children tend to grow faster in the spring.",
    "Sliced bread was invented a year after the invention of TV.",
    "If you keep a goldfish in a dark room, it will eventually turn white.",
    "Bullfrogs do not sleep.",
    "A snail breathes through its foot.",
    "Fish cough.",
    "It took the creator of the Rubik's Cube one month to solve the cube after he created it.",
    "Japanese square watermelons aren't edible. They are purely ornamental!",
    "An ant's sense of smell is stronger than a dog's.",
    "Tigers have striped skin, not just striped fur. The stripes are like fingerprints—no two tigers have the same pattern.",
    "Elephants are the only mammal that can't jump.",
    "Alligators will give manatees the right of way if they are swimming near each other.",
    "Canned baked beans aren't baked but stewed.",
    "Despite their hump, camels have straight spines.",
    "Sunsets on Mars are blue.",
    "Digging a hole to China is actually possible if you start in Argentina.",
    "Mosquitoes have 47 teeth.",
    "A quarter of the bones in your body are in your feet.",
    "Brain waves can be used to power an electric train.",
    "The Boston Marathon didn't allow female runners until 1972.",
    "Pigs can get sunburned.",
    "A one-day weather forecast requires about 10 billion math calculations.",
    "Dead people can get goosebumps.",
    "The Mona Lisa has no eyebrows.",
    "A ten-gallon hat holds less than one gallon of liquid.",
    "The average raindrop falls at 7 mph.",
    "Guy Fawkes is the reason men are called “guys.”",
    "Lizards communicate by doing push-ups.",
    "A giant squid has eyes the size of a volleyball.",
    "The average American will eat 35,000 cookies in their lifetime.",
    "Beavers were once the size of bears.",
    "A pigeon's feathers weigh more than their bones.",
    "A crocodile can't move its tongue.",
    "Honeybees navigate using the Sun as their compass.",
    "If you sneeze traveling 60 mph, your eyes are closed for an average of 50 feet.",
    "Hawaii and California are the only American states to grow coffee commercially.",
    "The square dance is the official state dance of Washington.",
    "When dinosaurs roamed the earth, volcanos were erupting on the Moon.",
    "The only letters that don't appear on the periodic table are J and Q.",
    "A single strand of spaghetti is called a “spaghetto.”",
    "At birth, a baby panda is smaller than a mouse.",
    "In 1923, a jockey suffered a fatal heart attack mid-race. His horse finished and won the race, making him the first and only jockey to win a race after death.",
    "To protect themselves from poachers, African elephants have been evolving without tusks.",
    "A Polish doctor faked a typhus outbreak to save more than 8,000 people from Nazis.",
    "The spiked dog collar was invented by the ancient Greeks to protect their dogs from wolf attacks.",
    "No number before 1,000 contains the letter “A” when spelled out.",
    "The real word for the # symbol is not “hashtag”. It's “octothorpe”.",
    "The 100 folds in a chef's hat stand for 100 ways to cook an egg.",
    "Play-Doh was originally used as wallpaper cleaner.",
    "The Eiffel Tower can grow up to about 6 inches taller in the summer due to heat expansion.",
    "Scotland has more than 421 words for “snow”.",
    "A nickel (five-cent coin) is only made of 25% nickel. The other 75% is copper.",
    "Movie trailers originally played after the movie.",
    "The people who voiced Mickey and Minnie Mouse were married in real life.",
    "Most people cannot lick their elbows. (You probably just tried it.)",
    "You cannot sneeze with your eyes open.",
    "The acid in your stomach can dissolve steel.",
    "The human brain cannot feel pain.",
    "Human noses and ears never stop growing.",
    "Women's hearts beat faster than men's.",
    "Newborn babies are colorblind.",
    "Human teeth are as strong as shark teeth!",
    "Every human has a unique tongue print.",
    "Boys have fewer taste buds than girls.",
    "You cannot smell while you sleep.",
    "Brown is the most common eye color.",
    "The body's largest organ is skin.",
    "Romans used urine as mouthwash.",
    "Alexander the Great may have been buried alive.",
    "Cleopatra wasn't Egyptian—she was Greek.",
    "The Statue of Liberty was originally supposed to be located in the Suez Canal.",
    "Early Americans used corn cobs as toilet paper.",
    "Identical twins don't have the same fingerprints because of environmental factors in the womb.",
    "Earth's rotation is slowing, increasing the length of a day by about 1.8 seconds per century.",
    "Earlobes have no biological purpose.",
    "The largest piece of fossilized dinosaur poo discovered is over 30cm long and over two litres in volume.",
    "Mars isn't actually round; it's shaped more like a rugby ball.",
    "The Universe's average color is called 'Cosmic Latte'.",
    "The smallest flying mammal is the bumblebee bat, found in Thailand.",
    "The circulatory system is more than 60,000 miles long, enough to go around the Earth almost two and a half times.",
    "There are parts of Africa in all four hemispheres.",
    "Humans can distinguish approximately 10 million colors.",
    "The 'German' part of German chocolate cake comes from a person's name, Samuel German, who created the sweet baking chocolate formula.",
    "Just 0.007% of the Earth's water is usable for people.",
    "Only one number has the same amount of letters as its value: four.",
    "The number of pyramids in Sudan is over 255, more than double the number found in Egypt.",
    "A group of flamingos is called a flamboyance.",
    "Astronauts can taste the fine dust from the Moon.",
    "Platypuses look so weird that when scientists first discovered them, they thought it was a hoax.",
    "The world's oldest wooden wheel has been around for more than 5,000 years.",
]

# --- HTMX Component Templates (Partial HTML for dynamic updates) ---

JOKE_CARD_TEMPLATE = '''
<div class="card shadow-sm border-0 h-100" id="joke-card-container">
    <div class="card-body d-flex flex-column justify-content-between">
        <h5 class="card-title text-primary"><i class="bi bi-chat-square-text-fill"></i> Fresh Joke</h5>
        <p id="joke-text" class="card-text fs-4 fw-light text-center my-4">{{ joke }}</p>
        <button 
            class="btn btn-outline-primary w-100 mt-3"
            hx-get="/api/joke"
            hx-target="#joke-card-container"
            hx-swap="outerHTML"
            hx-indicator="#joke-card-container"
            title="Fetch a new joke without a full page reload"
        >
            <i class="bi bi-arrow-right-circle-fill"></i> Tell Me Another!
        </button>
         <i class="spinner-border spinner-border-sm text-primary htmx-indicator" role="status"></i>
    </div>
</div>
'''

MAGIC_CARD_TEMPLATE = '''
<div class="card shadow-sm border-0 h-100" id="magic-card-container" hx-trigger="load delay:10s" hx-get="/api/magic" hx-swap="outerHTML">
    <div class="card-body">
        <h5 class="card-title text-success"><i class="bi bi-magic"></i> Magic Number Generator</h5>
        <div class="text-center my-4">
            <span class="display-3 fw-bold text-success" id="magic-number">{{ magic_number }}</span>
        </div>
        <p class="text-center text-muted">
            Next number in: <span id="countdown" class="fw-bold">10</span>s 
            <i class="spinner-border spinner-border-sm text-success htmx-indicator" role="status"></i>
        </p>
        <h6 class="mt-4 mb-2">Last 5 Numbers:</h6>
        <ul class="list-group list-group-flush small" id="history-list">
            {% for num in magic_history %}
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <i class="bi bi-dot"></i> {{ num }}
                <span class="badge bg-secondary rounded-pill">{{ loop.index }}</span>
            </li>
            {% endfor %}
        </ul>
    </div>
</div>
'''

# To-Do List Item Partial Template - Used by ADD and TOGGLE endpoints
TODO_ITEM_TEMPLATE = '''
<li id="item-{{ item.id }}" class="list-group-item d-flex justify-content-between align-items-center 
    {% if item.done %}list-group-item-success text-decoration-line-through{% endif %}">
    
    <span class="flex-grow-1">
        {{ item.text }}
    </span>

    <div class="btn-group btn-group-sm" role="group">
        <button 
            class="btn {% if item.done %}btn-success{% else %}btn-outline-success{% endif %}"
            hx-post="/api/todo/toggle/{{ item.id }}" 
            hx-target="#item-{{ item.id }}" 
            hx-swap="outerHTML"
            hx-indicator="#todo-list-container"
            title="Mark as done/undone"
        >
            <i class="bi bi-check-lg"></i>
        </button>
        <button 
            class="btn btn-outline-danger"
            hx-delete="/api/todo/{{ item.id }}" 
            hx-target="#item-{{ item.id }}"
            hx-swap="outerHTML"
            hx-confirm="Are you sure you want to delete '{{ item.text }}'?"
            title="Delete task"
        >
            <i class="bi bi-trash-fill"></i>
        </button>
    </div>
</li>
'''

# To-Do List Full Template (Used for initial load only)
TODO_LIST_TEMPLATE = '''
<ul id="todo-list" class="list-group list-group-flush">
    {% for item in todo_list %}
        {{ todo_item(item) }}
    {% endfor %}
</ul>
'''

# Helper function for rendering the navbar links
def nav_link(text, href, active_name, icon):
    current_endpoint = request.url_rule.endpoint if request.url_rule else ''
    is_active = (active_name == 'jokes' and current_endpoint == 'jokes') or (active_name == current_endpoint)

    return f'''
    <a class="nav-link {'active' if is_active else ''}" 
       href="{href}" 
       hx-get="{href if href != '/' else '/jokes-content'}" 
       hx-target="#main-content" 
       hx-push-url="true"
       hx-swap="innerHTML">
       <i class="bi bi-{icon}"></i> {text}
    </a>
    '''

# Helper function for rendering a single todo item
def render_todo_item(item):
    # This renders the item template (which is an HTML string)
    return render_template_string(TODO_ITEM_TEMPLATE, item=item)

# Add helper functions to the Jinja environment
app.jinja_env.globals.update(nav_link=nav_link, todo_item=render_todo_item)


# --- Base HTML Template (Includes HTMX, better icons, and Bootstrap 5) ---
base_template = '''
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Fun Flask HTMX App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    <style>
        body { padding-top: 70px; transition: background-color 0.3s, color 0.3s; }
        [data-theme="dark"] { background-color: #121212; color: #e0e0e0; }
        [data-theme="dark"] .navbar { background-color: #1f1f1f !important; }
        [data-theme="dark"] .card { background-color: #1f1f1f; border-color: #333; }
        [data-theme="dark"] .list-group-item { background-color: #1f1f1f; border-color: #333; color: #e0e0e0; }
        .htmx-indicator { display: none; }
        .htmx-request .htmx-indicator { display: inline-block !important; }
        .btn-copy { cursor: pointer; }
        footer { margin-top: 3rem; padding: 1rem 0; text-align: center; font-size: 0.9rem; color: #666; }
        /* To-Do Specific styles for dark mode */
        [data-theme="dark"] .list-group-item-success { background-color: #145a32 !important; color: #e0e0e0; }
    </style>
</head>
<body hx-history="false"> 
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top shadow-sm">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/"><i class="bi bi-lightning-charge-fill me-2"></i>Fun Flask HTMX</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">{{ nav_link('Jokes', '/', 'jokes', 'emoji-laughing-fill') | safe }}</li>
        <li class="nav-item">{{ nav_link('Facts', '/facts', 'facts', 'lightbulb-fill') | safe }}</li>
        <li class="nav-item">{{ nav_link('To-Do List', '/todo', 'todo', 'list-check') | safe }}</li>
        <li class="nav-item">{{ nav_link('Magic Number', '/magic', 'magic', 'dice-5-fill') | safe }}</li>
        <li class="nav-item">{{ nav_link('Color Text', '/color', 'color', 'palette-fill') | safe }}</li>
        <li class="nav-item">{{ nav_link('Reverse Text', '/reverse', 'reverse', 'arrow-left-right') | safe }}</li>
        <li class="nav-item">{{ nav_link('Calculator', '/calc', 'calc', 'calculator-fill') | safe }}</li>
      </ul>
      <button id="dark-toggle" class="btn btn-outline-light btn-sm" title="Toggle between light and dark themes">
          <i class="bi bi-moon-fill me-1"></i> Dark Mode
      </button>
    </div>
  </div>
</nav>
<main class="container">
  <div id="main-content">
    {{ content|safe }}
  </div>
</main>
<footer>
  &copy; 2025 Fun Flask App — Crafted with ❤️ & HTMX
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
    // --- Dark mode toggle and persistence ---
    const toggleBtn = document.getElementById('dark-toggle');
    const htmlEl = document.documentElement;

    function setTheme(theme) {
        htmlEl.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        toggleBtn.innerHTML = theme === 'dark' 
            ? '<i class="bi bi-sun-fill me-1"></i> Light Mode' 
            : '<i class="bi bi-moon-fill me-1"></i> Dark Mode';
    }

    toggleBtn.addEventListener('click', () => {
        const current = htmlEl.getAttribute('data-theme');
        setTheme(current === 'light' ? 'dark' : 'light');
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    // Update active navbar link on HTMX navigation
    document.addEventListener('htmx:afterRequest', (event) => {
        const targetUrl = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const linkPath = new URL(link.href).pathname;
            
            // Match current URL with link path
            if (targetUrl === linkPath || (targetUrl === '/' && linkPath === '/')) {
                link.classList.add('active');
            }
        });
    });
</script>
</body>
</html>
'''


# --- Routes for Full Page Load (Initial load) ---

# FIX: Set endpoint to 'jokes' for consistency with nav_link helper
@app.route('/', endpoint='jokes')
def jokes_page(): 
    content = get_jokes_content()
    return render_template_string(base_template, content=content, active='jokes')

@app.route('/facts')
def facts_page():
    content = get_facts_content()
    return render_template_string(base_template, content=content, active='facts')

@app.route('/todo')
def todo_page():
    content = get_todo_content()
    return render_template_string(base_template, content=content, active='todo')

@app.route('/magic')
def magic_page():
    content = get_magic_content()
    return render_template_string(base_template, content=content, active='magic')

@app.route('/color')
def color_page():
    content = get_color_content()
    return render_template_string(base_template, content=content, active='color')

@app.route('/reverse')
def reverse_page():
    content = get_reverse_content()
    return render_template_string(base_template, content=content, active='reverse')

@app.route('/calc')
def calc_page():
    content = get_calc_content()
    return render_template_string(base_template, content=content, active='calc')

# --- HTMX Content Routes (Partial Content for dynamic updates) ---

@app.route('/jokes-content')
def get_jokes_content():
    joke = random.choice(jokes)
    return f'''
    <h1 class="mb-5 border-bottom pb-2">Fun & Games Dashboard</h1>
    <div class="row">
        <div class="col-md-6 mb-4">
            {render_template_string(JOKE_CARD_TEMPLATE, joke=joke)}
        </div>
        <div class="col-md-6 mb-4">
            <div class="card shadow-sm border-0 h-100 p-4">
                <h5 class="card-title text-info"><i class="bi bi-info-circle-fill"></i> App Info</h5>
                <p>This enhanced Flask app uses **HTMX** for a modern, responsive feel without complex JavaScript frameworks.</p>
                <ul class="list-unstyled">
                    <li><i class="bi bi-check-circle-fill text-success me-2"></i> **To-Do List**: Persistence via Flask Session.</li>
                    <li><i class="bi bi-check-circle-fill text-success me-2"></i> **Jokes**: Instant joke refresh.</li>
                    <li><i class="bi bi-check-circle-fill text-success me-2"></i> **Facts**: Get a random, new fact.</li>
                    <li><i class="bi bi-check-circle-fill text-success me-2"></i> **Calculator**: Server-side math with HTMX POST.</li>
                </ul>
            </div>
        </div>
    </div>
    '''

@app.route('/facts-content')
def get_facts_content():
    fact = random.choice(facts)
    return f'''
    <h1 class="mb-5 border-bottom pb-2">🧠 Random Facts</h1>
    <div class="row">
        <div class="col-md-8 mx-auto">
            <div class="card shadow-lg border-0 h-100 p-5 text-center" id="fact-card-container">
                <h5 class="card-title text-danger mb-4"><i class="bi bi-stars"></i> Did You Know?</h5>
                <p class="card-text fs-3 fw-normal" id="fact-text">{fact}</p>
                <button 
                    class="btn btn-lg btn-outline-danger mx-auto mt-4" 
                    style="width: 250px;"
                    hx-get="/api/fact"
                    hx-target="#fact-card-container"
                    hx-swap="outerHTML"
                    hx-indicator="#fact-card-container"
                >
                    <i class="bi bi-shuffle"></i> Give Me Another Fact
                </button>
                <i class="spinner-border text-danger htmx-indicator mt-3" role="status"></i>
            </div>
        </div>
    </div>
    '''
# --- TO-DO LIST CONTENT ROUTE (FIXED) ---
@app.route('/todo-content')
def get_todo_content():
    # Initialize todo_list if it doesn't exist
    if 'todo_list' not in session:
        session['todo_list'] = []

    # FIX: Ensure the full LIST template is rendered inside the container
    todo_list_html = render_template_string(TODO_LIST_TEMPLATE, todo_list=session.get('todo_list', []))
    
    return f'''
    <h1 class="mb-5 border-bottom pb-2">✅ Persistent To-Do List</h1>
    <div class="row">
        <div class="col-md-8 mx-auto" id="todo-list-container">
            <div class="card shadow-lg border-0 p-4">
                <form 
                    class="input-group mb-4"
                    hx-post="/api/todo/add" 
                    hx-target="#todo-list"
                    hx-swap="beforeend"
                    hx-on::after-request="this.reset();"
                >
                    <input type="text" name="task" class="form-control form-control-lg" placeholder="New task..." required>
                    <button class="btn btn-primary btn-lg" type="submit">
                        <i class="bi bi-plus-lg"></i> Add
                    </button>
                </form>

                {todo_list_html} 
                <i class="spinner-border text-primary htmx-indicator mt-3" role="status"></i>
            </div>
        </div>
    </div>
    '''
# --- END TO-DO LIST CONTENT ROUTE (FIXED) ---


@app.route('/magic-content')
def get_magic_content():
    magic_number = random.randint(1, 1000)
    history = session.get('magic_history', [])
    history.insert(0, magic_number)
    session['magic_history'] = history[:5]
    session.modified = True 
    
    return f'''
    <h1 class="mb-5 border-bottom pb-2">Magic Number</h1>
    <div class="row">
        <div class="col-md-6 mx-auto">
            {render_template_string(MAGIC_CARD_TEMPLATE, magic_number=magic_number, magic_history=session['magic_history'])}
        </div>
    </div>
    '''

@app.route('/color-content')
def get_color_content():
    return f'''
    <h1 class="mb-5 border-bottom pb-2">🎨 Color Text Cycler (FIXED)</h1>
    <div class="card shadow-lg border-0 p-5 text-center">
        <h2 id="color-text" class="display-4 fw-bold mb-4">This text changes color!</h2>
        <button id="toggle-color" class="btn btn-lg btn-outline-secondary mx-auto" style="width: 280px;">
            <i class="bi bi-pause-fill me-2"></i> Pause Color Cycle
        </button>
    </div>
    <script>
    // --- Client-side JS for Color Cycler ---
    const colors = {colors};
    let index = 0;
    let cycling = true;
    const textEl = document.getElementById('color-text');
    const toggleBtn = document.getElementById('toggle-color');
    let colorInterval; 

    function cycleColor() {{
        if (!cycling || !textEl) return;
        textEl.style.color = colors[index];
        index = (index + 1) % colors.length;
    }}
    
    function startCycle() {{
        if (colorInterval) clearInterval(colorInterval);
        colorInterval = setInterval(cycleColor, 750); // Faster cycle
        cycleColor();
    }}

    toggleBtn.addEventListener('click', () => {{
        cycling = !cycling;
        if (cycling) {{
            toggleBtn.innerHTML = '<i class="bi bi-pause-fill me-2"></i> Pause Color Cycle';
            startCycle();
        }} else {{
            toggleBtn.innerHTML = '<i class="bi bi-play-fill me-2"></i> Resume Color Cycle';
            clearInterval(colorInterval);
        }}
    }});

    startCycle();

    document.addEventListener('htmx:beforeSwap', (evt) => {{
        if (evt.detail.target.id === 'main-content' && window.location.pathname === '/color') {{
            clearInterval(colorInterval);
        }}
    }});
    </script>
    '''

@app.route('/reverse-content')
def get_reverse_content():
    return '''
    <h1 class="mb-5 border-bottom pb-2">🔠 Text Reverser Utility</h1>
    <div class="row">
        <div class="col-md-8 mx-auto">
            <div class="card shadow-lg border-0 p-4">
                <div class="mb-3">
                    <label for="text" class="form-label fs-5"><i class="bi bi-input-cursor-text"></i> Enter text:</label>
                    <input type="text" id="text" name="text" class="form-control form-control-lg" autocomplete="off" placeholder="Type here for instant reverse..." />
                </div>
                <div class="d-flex align-items-center justify-content-between mt-4 border-top pt-3">
                    <h3 class="mb-0">Reversed: <span id="reversed-text" class="text-primary fw-bold"></span></h3> 
                    <button id="copy-btn" class="btn btn-outline-primary btn-lg btn-copy" disabled>
                        <i class="bi bi-clipboard-fill me-1"></i> Copy
                    </button>
                </div>
            </div>
        </div>
    </div>
    <script>
    // --- Client-side JS for Text Reverser ---
    const input = document.getElementById('text');
    const output = document.getElementById('reversed-text');
    const copyBtn = document.getElementById('copy-btn');

    input.addEventListener('input', () => {
        const val = input.value;
        const reversed = val.split('').reverse().join('');
        output.textContent = reversed;
        copyBtn.disabled = reversed.length === 0;
    });

    copyBtn.addEventListener('click', () => {
        if(output.textContent.length === 0) return;
        navigator.clipboard.writeText(output.textContent)
            .then(() => {
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> Copied!';
                setTimeout(() => copyBtn.innerHTML = originalText, 1500);
            });
    });
    </script>
    '''

@app.route('/calc-content')
def get_calc_content():
    return '''
    <h1 class="mb-5 border-bottom pb-2">🔢 Simple Calculator</h1>
    <div class="row">
        <div class="col-md-6 mx-auto">
            <div class="card shadow-lg border-0 p-4">
                <form hx-post="/api/calculate" hx-target="#calc-result" hx-indicator="#calc-indicator" hx-swap="innerHTML">
                    <div class="row g-3 mb-3">
                        <div class="col-md-5">
                            <input type="number" name="num1" class="form-control form-control-lg" placeholder="First Number" required>
                        </div>
                        <div class="col-md-2">
                            <select name="operation" class="form-select form-select-lg" required>
                                <option>+</option>
                                <option>-</option>
                                <option>*</option>
                                <option>/</option>
                            </select>
                        </div>
                        <div class="col-md-5">
                            <input type="number" name="num2" class="form-control form-control-lg" placeholder="Second Number" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg w-100">
                        Calculate <i class="bi bi-arrow-right-circle-fill"></i>
                    </button>
                </form>
                <div class="text-center mt-4 border-top pt-3">
                    <h4 class="text-muted mb-0">Result:</h4>
                    <h2 id="calc-result" class="display-5 text-primary fw-bold mt-2">0</h2>
                    <i id="calc-indicator" class="spinner-border text-primary htmx-indicator mt-3" role="status"></i>
                </div>
            </div>
        </div>
    </div>
    '''

# --- API Routes (Used by HTMX) ---

@app.route('/api/joke')
def api_joke_htmx():
    last_joke_index = session.get('last_joke_index', -1)
    
    available_jokes = [j for i, j in enumerate(jokes) if i != last_joke_index]
    
    if available_jokes:
        joke = random.choice(available_jokes)
    else:
        joke = jokes[0] if jokes else "No jokes found!"

    try:
        new_index = jokes.index(joke)
        session['last_joke_index'] = new_index
    except ValueError:
        session['last_joke_index'] = -1
        
    session.modified = True 
    return render_template_string(JOKE_CARD_TEMPLATE, joke=joke)

@app.route('/api/fact')
def api_fact_htmx():
    fact = random.choice(facts)
    return f'''
    <div class="card shadow-lg border-0 h-100 p-5 text-center" id="fact-card-container">
        <h5 class="card-title text-danger mb-4"><i class="bi bi-stars"></i> Did You Know?</h5>
        <p class="card-text fs-3 fw-normal" id="fact-text">{fact}</p>
        <button 
            class="btn btn-lg btn-outline-danger mx-auto mt-4" 
            style="width: 250px;"
            hx-get="/api/fact"
            hx-target="#fact-card-container"
            hx-swap="outerHTML"
            hx-indicator="#fact-card-container"
        >
            <i class="bi bi-shuffle"></i> Give Me Another Fact
        </button>
        <i class="spinner-border text-danger htmx-indicator mt-3" role="status"></i>
    </div>
    '''

@app.route('/api/todo/add', methods=['POST'])
def api_todo_add():
    task = request.form.get('task')
    if not task:
        return "" 
    
    new_item = {
        'id': str(uuid.uuid4()),
        'text': task,
        'done': False
    }
    
    todo_list = session.get('todo_list', [])
    todo_list.append(new_item)
    session['todo_list'] = todo_list
    session.modified = True 
    
    return render_template_string(TODO_ITEM_TEMPLATE, item=new_item)

@app.route('/api/todo/toggle/<item_id>', methods=['POST'])
def api_todo_toggle(item_id):
    todo_list = session.get('todo_list', [])
    
    item_to_update = next((item for item in todo_list if item['id'] == item_id), None)
    
    if item_to_update:
        item_to_update['done'] = not item_to_update['done']
        session.modified = True 
        
        return render_template_string(TODO_ITEM_TEMPLATE, item=item_to_update)
        
    return make_response("Task not found", 404)


@app.route('/api/todo/<item_id>', methods=['DELETE'])
def api_todo_delete(item_id):
    todo_list = session.get('todo_list', [])
    
    updated_list = [item for item in todo_list if item['id'] != item_id]
    session['todo_list'] = updated_list
    session.modified = True 
    
    return make_response("", 200)

@app.route('/api/magic')
def api_magic_htmx():
    magic_number = random.randint(1, 1000)
    history = session.get('magic_history', [])
    
    history.insert(0, magic_number)
    session['magic_history'] = history[:5]
    session.modified = True 
    
    return render_template_string(MAGIC_CARD_TEMPLATE, magic_number=magic_number, magic_history=session['magic_history'])

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        num1_str = request.form.get('num1')
        num2_str = request.form.get('num2')
        operation = request.form.get('operation')
        
        if not num1_str or not num2_str or not operation:
             return '<p class="text-danger fw-bold mt-2">Error: Missing input fields.</p>'
        
        num1 = float(num1_str)
        num2 = float(num2_str)
        result = 0

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                return f'<p class="text-danger fw-bold mt-2">Error: Division by zero!</p>'
            result = num1 / num2
        
        if isinstance(result, float) and not result.is_integer():
            result = round(result, 3)
        else:
            result = int(result)
            
        return f'<h2 id="calc-result" class="display-5 text-primary fw-bold mt-2">{result}</h2>'
        
    except ValueError:
        return '<p class="text-danger fw-bold mt-2">Error: Invalid number input. Please enter valid numbers.</p>'
    except Exception as e:
        return f'<p class="text-danger fw-bold mt-2">Error: General Calculation Error ({str(e)})</p>'


# --- Error Handler ---

@app.errorhandler(404)
def page_not_found(e):
    page_content = '''
    <div class="text-center mt-5">
      <h1 class="display-1 text-danger">404</h1>
      <h2 class="mb-4">Page Not Found</h2>
      <p>Oops! The page you are looking for does not exist.</p>
      <a href="/" class="btn btn-primary btn-lg"><i class="bi bi-house-door-fill me-2"></i>Go Home</a>
    </div>
    '''
    # Correct endpoint name for active link logic
    return make_response(render_template_string(base_template, content=page_content, active='404'), 404)

# --- Run App ---

if __name__ == '__main__':
    print("Starting Flask App with HTMX enhancements...")
    app.run(debug=True, host='0.0.0.0')