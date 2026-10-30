from flask import Flask, render_template, request, session
from projects.stacks import Stack
from projects.infix_postfix import infix_to_postfix
from projects.socials import register_socials
from projects.linked_list import LinkedList
from projects.queue import Queue
from projects.dequeue import DeQueue


app = Flask(__name__)
register_socials(app)

linked_list = LinkedList()
app.secret_key = "change-this-to-a-random-secret-key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


# Works tablet homepage
@app.route('/works')
def works():
    return render_template('works.html')


# Convert string to uppercase
@app.route('/works/uppercase', methods=['GET', 'POST'])
def uppercase():
    result = None

    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()

    return render_template('touppercase.html', result=result)


# Calculate the area of a circle
@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None

    if request.method == 'POST':
        radius = request.form.get('radius', '')

        try:
            radius = float(radius)

            if radius < 0:
                result = "Radius cannot be negative."
            else:
                result = 3.14 * radius * radius

        except ValueError:
            result = "Please enter a valid radius."

    return render_template('circle.html', result=result)


# Calculate the area of a triangle
@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None

    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')

        try:
            base = float(base)
            height = float(height)

            if base < 0 or height < 0:
                result = "Base and height cannot be negative."
            else:
                result = 0.5 * base * height

        except ValueError:
            result = "Please enter a valid base and height."

    return render_template('triangle.html', result=result)



# Stack operations using a linked list
@app.route('/works/stacks', methods=['GET', 'POST'])
def stacks():
    stack = Stack()

    # Restore the saved values into the linked-list stack.
    for value in reversed(session.get('stack_elements', [])):
        stack.push(value)

    message = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'push':
            value = request.form.get('value', '').strip()

            if value:
                stack.push(value)
                message = f"Pushed {value} onto the stack."
            else:
                message = "Please enter a value."

        elif action == 'pop':
            value = stack.pop()

            if value is not None:
                message = f"Popped: {value}"
            else:
                message = "Stack is empty."

        elif action == 'peek':
            value = stack.peek()

            if value is not None:
                message = f"Top element: {value}"
            else:
                message = "Stack is empty."

    # Save values from top to bottom for the next request.
    session['stack_elements'] = stack.get_elements()

    return render_template(
        'stacks.html',
        elements=stack.get_elements(),
        message=message
    )

# Infix to Postfix
@app.route('/works/infix-postfix', methods=['GET', 'POST'])
def infix_postfix():
    result = None
    error = None

    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()

        if expression:
            try:
                result = infix_to_postfix(expression)
            except ValueError as e:
                error = str(e)
        else:
            error = "Please enter an expression."

    return render_template(
        'infix_postfix.html',
        result=result,
        error=error
    )


# Linked List Activity
@app.route('/works/linked-list', methods=['GET', 'POST'])
def linked_list_page():
    message = None

    if request.method == 'POST':
        action = request.form.get('action')
        value = request.form.get('value', '').strip()

        if action in ('add', 'add_beginning', 'delete', 'search'):
            if not value:
                message = "Please enter a value."
            else:
                if action in ('add', 'add_beginning'):
                    if action == 'add_beginning':
                        linked_list.add_at_beginning(value)
                    else:
                        linked_list.add(value)

                    message = f"Added {value} successfully."

                elif action == 'delete':
                    if linked_list.delete(value):
                        message = f"Deleted {value} successfully."
                    else:
                        message = f"{value} was not found."

                elif action == 'search':
                    position = linked_list.search(value)

                    if position is not None:
                        message = f"{value} found at position {position}."
                    else:
                        message = f"{value} was not found."

        elif action == 'delete_beginning':
            deleted = linked_list.delete_at_beginning()

            if deleted is not None:
                message = f"Deleted {deleted} from the beginning."
            else:
                message = "The linked list is empty."

    return render_template(
        'linked_list.html',
        nodes=linked_list.get_elements(),
        message=message
    )

@app.route('/works/queue', methods=['GET', 'POST'])
def queue_page():
    queue = Queue()
    elements = session.get('queue_elements', [])

    for item in elements:
        queue.enqueue(item)

    message = ""

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'enqueue':
            value = request.form.get('value', '').strip()

            if value:
                queue.enqueue(value)
                message = f"{value} added to the queue."
            else:
                message = "Please enter a value."

        elif action == 'dequeue':
            removed = queue.dequeue()

            if removed is None:
                message = "The queue is empty."
            else:
                message = f"{removed} removed from the queue."

        elif action == 'peek':
            front_item = queue.peek()

            if front_item is None:
                message = "The queue is empty."
            else:
                message = f"Front item: {front_item}"

        elements = queue.display()
        session['queue_elements'] = elements

    return render_template(
        'queue.html',
        elements=queue.display(),
        message=message
    )

@app.route('/works/dequeue', methods=['GET', 'POST'])
def dequeue_page():
    queue = DeQueue()

    elements = session.get('dequeue_elements', [])

    for item in elements:
        queue.enqueue(item)

    message = ""

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'enqueue':
            value = request.form.get('value', '').strip()

            if value:
                queue.enqueue(value)
                message = f"{value} added."
            else:
                message = "Please enter a value."

        elif action == 'dequeue':
            removed = queue.dequeue()

            if removed is None:
                message = "The queue is empty."
            else:
                message = f"{removed} removed from the front."

        elements = queue.display()
        session['dequeue_elements'] = elements

        return render_template(
                'dequeue.html',
                elements=queue.display(),
                message=message
            )
        
@app.route('/works/sorting')
def sorting_menu():
    return render_template('sorting_menu.html')

 
@app.route('/works/sorting/bubble')
def bubble_sort():
    return render_template('bubble_sort.html')


@app.route('/works/sorting/selection')
def selection_sort():
    return render_template('selection_sort.html')


@app.route('/works/sorting/insertion')
def insertion_sort():
    return render_template('insertion_sort.html')


@app.route('/works/sorting/quick')
def quick_sort():
    return render_template('quick_sort.html')

@app.route('/works/sorting/merge')
def merge_sort():
    return render_template('merge_sort.html')

  
if __name__ == "__main__":
    app.run(debug=True)
