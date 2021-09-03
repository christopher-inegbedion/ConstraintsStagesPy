# Stages/Constraints
## About the project
Stages and Constraints provide a platform for numerous jobs/processes/services to be created and executed. The Stages and Constraints provide a means to automate familiar processes and return some useful output.

This aim of this project is to provide a means by which different services and processes can be combined and connected together to form a cohesive unit that solves a problem, or provide a unique experience.

The idea was to provide a means for "lego-like" means of customisation where 1 or more constraints could be combined to create unique experiences for the users.
## Constraints
A constraint is a process that accepts some **INPUT**, passes it to its **MODEL** and produces some **OUTPUT** at the end. Constraints can be mixed and matched together to provide a variety of possible outcomes/possibilities. They can be as simple or complex as required, with some constraints being able to accept more than 1 output while others accept none and still produce some **OUTPUT**

### Creating a constraint
A constraint has 2 basic requirements which are its name and a model. To create a constraint the `CustomConstraint` class is used and then a name, description and any model is passed to it.
```python
# This is an example of a basic constraint
name = "Test constraint"
desc = "description"
model = TestModel()

constraint = CustomConstraint(name, desc, model)
```
A major part of a constraint's operation involves its **MODEL**, this performs the work of the constraint and, describes what the constraint does, the types of input(s) the constraint is allowed to accept, the type of output that will be returned, etc. Hence there is only a single class for creating a constraint (`CustomConstraint`), all that needs to be provided to it is its name and the model it'll utilise, (optionally a custom **FLAG** can also be set). On the other hand, there are numerous **MODEL**'s that each perform a specific job and can be used by any constraint.

## Why have **INPUT**, **MODEL** and **OUTPUT** been highlighted?

Key to understanding the way a constraint functions is understanding the roles of its 3 core components: **INPUT**, **MODEL**, and **OUTPUT**. There is a 4th component which is the **FLAG**, but this will be covered later. Of the 3 core components, the most important one is the **MODEL**, as it is through this that the constraint knows what it will need to accept as **INPUT** and what it will eventually produce as **OUTPUT**.  These 3 each have to be correctly configured in order for a constraint to work properly.   The 3 components are explained further below:

1. **INPUT**: The main/only purpose of this component is to retrieve the input(s) required by the model from the user. This could be from the console, through function calls or both. The **MODEL** dictates what will be inputted into the console, how much input will be required, how the input will be inputted, etc.
	
	Some models do not require for input to be retrieved once the constraint begins and but **INPUT** can be requested once the **MODEL** has begun(This is explained further below).
	
2. **MODEL**: The purpose of this component is to perform some work on the inputs it requires. Each model has its own set of requirements and the job it does will also be different from that of other models. The model is attached to a constraint and thus once a constraint begins and the inputs have been retrieved it is up to the model to process the received input and produce some useful output from it.

3. **OUTPUT**: The purpose of this component is to deliver the final output. Once a model has completed its work it saves it resulting **OUTPUT** as can be used to perform any function with. The model specifies the type of output it will produce(string, boolean, integer, etc) and that will correspond with the type of output that is eventually produced.

> NOTE: In code, the components are not tightly labelled as INPUT, MODEL and OUTPUT, the logical flow from the input through to the output is implicitly documented in the code.

## INPUT
The **INPUT** component is the first part of the constraint, it gathers the inputs from the users and sends them to the **MODEL**. In this section all the aspects regarding to a model's input requirements will be covered. 

>The data passed to a constraint's **MODEL** is in the form of an array. So if a **MODEL** requires more than 1 input from the user, all the inputs passed to the constraint would be put in an array. The same applies to models with just a single input required.

#### Initial input requirement
The first part to be covered has to do with input collection. Depending on the model used by the constraint it might require that input is fed into the constraint when it begins or it could request for input(s) once the constraint has already begun. 

In a constraint the parameter that determines whether or not it will require initial input from the constraint is the `initial_input_required` field. If this value is True then the constraint will have to be provided with input before the model is begun, however if the value is false, input can still be provided, but only through input requests. Below are examples of 2 models, one requires input from the beginning whilst the other does not.

For the constraint below, regardless of the input mode(to be covered later), if input is not provided before the model begins then an error message will be displayed.
```python
# Input required once constraint starts.
# -
# Disclaimer: '```' signifies that some parts that are not useful for this example are hidden
------------
->test_model.py

class TestModel(Model):
	def __init__(self):
		```
		self.initial_input_required = True
		```
------------

------------
>main.py

name = "test constraint"
model = TestModel()
constraint = CustomConstraint(name, model)
constraint.add_input(2)
constraint.start()
------------

```

For the constraint below, initial input is not required and thus to get input from the user, an input request is used.
```python
# Input not required once constraint starts.
# -
# Disclaimer: '```' is to hide other aspects of the model's creation that are not useful for this example
------------
>test_model.py

class TestModel(Model):
	def __init__(self):
		```
		self.initial_input_required = False
		```
	def run(self, inputs):
		```
		# Due to the fact that initial input is disabled. The only
		# way to retrieve input is through a call to the request_input() method
		user_input = self.request_input()  # input request
		```
		
------------

------------
>main.py

name = "test constraint"
model = TestModel()
constraint = CustomConstraint(name, model)
constraint.start()
------------

```

### Providing **INPUT** to the constraint
---
Before a model can be started, there are a number of requirements it might have in regards to its **INPUT** that have to be provided to the constraint in order for it to run smoothly. These requirements are covered below.

**Input type**
First is the input type. This defines the type of input the model is able to accept. There are 2 categories for input types. First is the regular, single input type (i.e `INT`, `BOOL`, etc) and then next is the mixed type.

Following that we have those the mixed input type. For these input types (some of which include `LIST_AND_INT`, `LIST_AND_BOOL`, etc, they all accept a list/array of values as their first input (provided through a function call) and then a regular input as its second. Mixed input types are best used with the `MIXED_USER_PRE_DEF` input mode.

It should be noted that regardless of the amount of inputs required by a **MODEL**, they will each have to be of the same type, otherwise it will result in an error. An example of this is if a **MODEL** requires 5 inputs, and has an `INT` as its input type, then each of those 5 inputs will have to be of the type `INT`.

All the available input types include:
- `INT`: Accepts an integer as input
- `BOOL`: Accepts a boolean as input
- `STRING`: Accepts a string as input
- `CONSTRAINT`: Accepts a constraint as input
- `LIST_AND_BOOL`: Accepts a list and boolean as input
- `LIST_AND_INT`: Accepts a list and integer as input
- `LIST_AND_STRING`: Accepts a list and string as input
- `LIST_AND_CONSTRAINT`: Accepts a list and constraint as input

### Input mode
The input mode describes how the model retrieves its inputs, this could be through the console, function calls or both.
There are 3 basic modes for input reception a **MODEL** has, these include: `USER`, `CONSTRAINT` and `PRE_DEF`. The last mode (`PRE_DEF`) is a mixture of the `USER` and `PRE_DEF` mode. With the modes listed, it is important to note that if initial input is not required by the model, then the only way of input provision for a model will be through input requests by the model. The input modes available are defined below: 
1. `USER`: With this mode, input is provided to the constraint through the console.
2. `PRE_DEF`: With this mode, input is provided through a function call provided by the constraint: `add_input(data)`
3. `CONSTRAINT`: -under construction-
4. `MIXED_USER_PRE_DEF`: With this mode, inputs can provided by both the console and function calls. In this mode the first input received by the constraint has to be through a function call, and then subsequent inputs can be through the console or through further function calls.

### Input count
This part has to do with the amount of inputs a **MODEL** requires. The parameter used to handle this by the model is `input_count`. The number of inputs provided to the constraint, has to be exactly the amount specified in the `input_count` parameter, otherwise it will result in an error. 

```python
class TestModel(Model):
	```
	self.input_type = InputType.INT
	# The model will require 5 inputs to be provided to it
	self.input_count = 5
	```
```
**Automatic input count**
With all that said, the amount of inputs required by a **MODEL** does not have to be so rigid. The amount can be set to dynamically increase in line with the requirements of the model. What this means is that even after the `input_count` value has been set, before the constraint has begun, an arbitrary number of inputs can be provided to the constraint, which will then effectively result in the `input_count` parameter being overwritten by the amount of input provided before the model is started. 

It is best to set the `input_count` parameter to 0 if the input count is expected to grow.

It is important to note that whilst it is possible for the input count to grow. For this to take effect, the input mode has to be `PRE_DEF`, because the `USER` input mode takes effect when the model begins and thus needs to know how much input is required beforehand.
```python
# TestModel() in this example would normally expect 2 
# inputs to be provided to it through a function call, 
# but because the set_input_count_growable() method is called,
# then an arbitrary number of inputs can be passed
name = "Test constraint"
model = TestModel()

model.set_input_count_growable()
model.add_input(1)
model.add_input(2)
model.add_input(3)
...
```

The following code above would not lead to an error because the `set_input_count_growable()` method is called, hence any number of inputs can be added. This can be enabled by calling the `set_input_count_growable()` method provided by the model before it is started.

**Manual input count**
Given the fact that dynamically increasing input counts have no effect for models that require input from the console (i.e `USER` input type), the other method for overwriting the set `input_count` parameter is by manually specifying how much input will be passed.

This is done using the `set_input_count(count)` method provided by the model. This allows for the input count to be changed before the model is begun. 

This method of dynamic input count manipulation can be utilised by any input mode.

```python
# TestModel() in this example would normally expect 2 
# inputs to be provided to it through a function call, 
# but through the set_input_count(count) method, this
# value can be changed.
name = "Test constraint"
model = TestModel()

model.set_input_count(3)
model.add_input(1)
model.add_input(2)
model.add_input(3)
...
```
The example above would result in the model accepting 3 inputs as opposed to the 2 originally assigned.

This covers the basic aspects as regards to accepting input for the model.


## MODEL
The **MODEL** is the heartbeat of a constraint, and without it, a constraint cannot function. A **MODEL** with/without **INPUT**, does some work and then provides some output. Although it is possible for a **MODEL** to not receive input, it is required that the **MODEL** produces some sort of **OUTPUT** at the end of its execution, failure to do so will result in an error.

### Starting a model
---
In order to begin a **MODEL**, its `run(data)` method has to be called. This is what kickstarts the **MODEL** and begins all the work done by the model. This method is called from a constraint.

The code below illustrates how a model that is started from a constraint:
```python
# In a constraint its model is begun by calling its run(data) method, along with any data, if required. The data is the input provided.
class CustomConstraint(Constraint):
	def start(self):
		```
		# begins the model  
		self.model.run(self.inputs)
	```
```
From the example above, the **MODEL** is started by calling `run(data)` in the `start()` method of a constraint, the inputs provided are also passed. This is the simplest illustration as to how a model is begun, of course there are some steps that have been hidden for simplicity (e.g verification) but for the most part, the model is begun through a call to its `run(data)` method from the constraint's `start()` method.

**Performing work**
In order for a model to be useful it has to perform some work. The work of a **MODEL** is done in its `run(data)` method. From this method all the required computation can be carried out, and at the end some output will be produced.

Other methods can be called from the `run(data)` method to perform different tasks, but regardless of which external methods are used the final output is passed from the model's `run(data)` method.

Below is an example of a `run(data)` method in a constraint. The model is very simple, it takes 2 integer inputs, multiplies them and returns an integer as output. The constraint does require initial input before it is run. The input mode is not important in this example as any mode would be sufficient.

```python
>test_model.py

class TestModel(Model):
	def __init__(self):  
		```
	    self.name = "Test"  
	    self.input_type = InputType.INT  
	    self.input_count = 2  
		self.output_type = InputType.INT  
		```
  
    super().__init__(self.name, self.model_family, self.input_type, self.input_mode, self.input_count,  
                     self.output_type, initial_input_required=self.initial_input_required,)

	def run(self, inputs: list):
		super().run(inputs)
		
		# The input passed from the constraint to the model is an array
		input1 = inputs[0]
		input2 = inputs[1]
		
		# Multiply the numbers and produce the output
		result = input1*input2
		
		# Pass the output to end the model
		self._complete(result)
	
	def _complete(self, data, aborted=False):  
	    super()._complete(data)

```
That's all that is required to create a model that accepts 2 integer values, multiplies them and returns an integer as its output. All the work done by the model is done in the `run(data)` method.

In more complex models, multiple functions aside from the `run(data)` method can be utilised to perform various tasks, but the final output is passed through the `run(data)` method.

#### Model family
There are 2 families for a model, first is the `COMBINED_CONSTRAINT` model and the other is the `CONSTRAINT` model.

The `COMBINED_CONSTRAINT` model accepts only constraints as its input, and thus this type of model is only used by combined constraints(i.e constraints that accept other constraints as input). The model can have its rules for constraints that are to be added to it, and for those that do not meet that rule, the `abort(msg)` function is available to alert the user of a wrong input. `COMBINED_CONSTRAINT` model's can only accept their inputs through function calls, thus the input type of the model has to be `PRE_DEF`.

`COMBINED_CONSTRAINT` models can only accept constraints that have initial input enabled. This is because one of the main attributes of combined constraints is its ability to pass its output as input to the next constraint, and a constraint that does not accept input before its model is begun will not be able to make great effect of that rule.

The other is the `CONSTRAINT` model and this accepts all input types excluding constraints, this type of model is used by constraints that do some work and produce its output. This is the regular type of model that accepts traditional input types(e.g integer, boolean, string, etc) and produces output from it.

#### Requesting input
It is possible for a model to request for **INPUT** from the user, while it is performing some work. For models that do not have initial input enabled, the only method for data collection is through input requests.

The input mode for input requests is through the console (May be subject to change).

In order to request input, the `request_input()` method is used. The code below illustrates how input could be requested:

```python
# The model below uses input requests to get input.

class TestModel(Model):
	```
	def run(self, inputs: list):
		```
		user_input = self.request_input()
		``` 
```

## OUTPUT
This is the final component of a constraint. This part is quite straight-forward as once a model has completed execution is stores its result in the constraints `output` field. A model can only have a singular input.

The result type returned by a **MODEL** has to be the same as the result type specified in its configuration, if both types where different, this would lead to an error.

Last update: 28 Jan 2020
