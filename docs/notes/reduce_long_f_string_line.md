# Reduce Long F-String Line

* [Reduce Long F-String Line](#reduce-long-f-string-line)
  * [Problem](#problem)
  * [Solution](#solution)
  * [Example](#example)
  * [References](#references)

* Current Dunder String Method: `__str__`

    ```python
    def test_dunder_string_method(self):
    """
    Test that the dunder str method is correct.
    """
    self.assertEqual(
        str(self.cognative_distortion),
        (
            f"{self.cognative_distortion.name} "
            f"--- "
            f"{self.cognative_distortion.description[:57] + '...' if len(self.cognative_distortion.description) > 57 else self.cognative_distortion.description}"
        ),
    )    
    ```

* Refactor the following:

    ```python
    f"{self.cognative_distortion.description[:57] + '...' if len(self.cognative_distortion.description) > 57 else self.cognative_distortion.description}"
    ```
* To:

    ```python
    description = self.cognative_distortion.description
    if len(description) > 57:
        description = description[:57] + '...'
    result = f"{self.cognative_distortion.name} --- {description}"
    ```