# Static Methods

Static methods are methods that are bound to a class rather than its object. They do not require a class instance creation. So, they are not dependent on the state of the object.

The syntax of static methods is similar to the syntax of class methods. The difference is that a static method has no `self` parameter to access class attributes.

## Removed Static Methods

- `vitals.models.BloodPressure.get_average_and_median`

    ```python
    from statistics import median

    # ...

    class BloodPressure(CreatedUpdatedBase):
        # ...

        # Use the `@staticmethod` decorator to define a static method.
        # A `static method` is a method that doesn't need to be called on an
        # instance of the class.
        # An `instance of the class` means an object created from the class.
        # A `static method` is a method that doesn't need `self` as the first
        # argument.
        # A `BloodPressure` object is not needed to call the
        # `get_average_and_median` method.
        # a_specific_blood_pressure_object =
        # BloodPressure.objects.get(systolic=120, diastolic=80) is not needed.
        # BloodPressure.get_average_and_median() is enough.
        @staticmethod
        def get_average_and_median():
            """
            Method to get the average and median of the systolic and diastolic
            blood pressure readings of all the `systolic` and `diastolic`
            values of `BloodPressure` objects.
            """
            systolic_values = BloodPressure.objects.values_list(
                "systolic",
                flat=True,
            )
            diastolic_values = BloodPressure.objects.values_list(
                "diastolic",
                flat=True,
            )
            if len(systolic_values) == 0:
                return {
                    "systolic_average": None,
                    "diastolic_average": None,
                    "systolic_median": None,
                    "diastolic_median": None,
                }
            else:
                systolic_average = sum(systolic_values) / len(systolic_values)
                diastolic_average = sum(diastolic_values) / len(diastolic_values)
                systolic_median = median(systolic_values)
                diastolic_median = median(diastolic_values)
            return {
                "systolic_average": round(systolic_average, 2),
                "diastolic_average": round(diastolic_average, 2),
                "systolic_median": round(systolic_median, 2),
                "diastolic_median": round(diastolic_median, 2),
            }
        # ...
    ```

## Examples of Static Methods

```python
class ExampleClass:
    @staticmethod
    def static_method():
        print("Static method has been called.")
```

Static methods are used to access class attributes from outside the class. They don't have access to the `self` parameter because they are not bound to a class instance.

```python
class ExampleClass:
    @staticmethod
    def static_method():
        print("Static method has been called.")

ExampleClass.static_method()
```

## Static Methods vs. Class Methods

Static methods are similar to class methods. The difference is that a class method takes the `cls` parameter to access class attributes. Static methods don't have access to the `cls` parameter.

## Static Methods vs. Instance Methods

Static methods are similar to instance methods. The difference is that an instance method takes the `self` parameter to access instance attributes. Static methods don't have access to the `self` parameter.

## Static Methods vs. Global Functions

Static methods are similar to global functions. The difference is that a static method is bound to a class. Global functions are not bound to a class.

