import math as maths

class ProgressBar:
    def __init__(self, target, task_text = None, bar_length = 20):
        self.target     = target
        self.task_text  = task_text
        self.bar_length = bar_length

        self.value      = 0
        self._finished  = False

        self._render(initial = True)

    def __iadd__(self, delta):
        self.update(self.value + delta)
        return self

    def update(self, value):
        if value > self.value:
            if value > self.target:
                raise "ProgressBar: Value cannot be greater than target. Noob."
            elif value == self.target:
                self._finished = True

            self.value = value
            self._render()

    def _bar_string(self):
        num_filled = maths.floor(              self.value  / self.target * self.bar_length)
        num_empty  = maths.ceil((self.target - self.value) / self.target * self.bar_length)

        return "{}{}".format("#" * num_filled, "-" * num_empty)

    def _num_string(self):
        tar_str = str(self.target)
        val_str = str(self.value ).rjust(len(tar_str))

        return "{}/{}".format(val_str, tar_str)


    def _render(self, initial = False):
        if self.task_text != None:
            print("\r{}: {} [{}]".format(self.task_text, self._num_string(), self._bar_string()), end="")
        else:
            print("\r{} [{}]".format(self._num_string(), self._bar_string()), end="")

        if self._finished:
            print()

def enumerate_with_progress(enumerable, **kwargs):
    """A generator that takes an enumerable, and does a progressbar while generating through it

    Will loop forever if given an infinite generator!
    Will keep all items in memory - watch out for massive enumerables!
    """
    xs = list(enumerable) # Have to evaluate everything ahead-of-time, so we know the length

    pb = ProgressBar(len(xs), **kwargs)

    for x in xs:
        yield x
        pb += 1

if __name__ == "__main__":
    import time

    for x in enumerate_with_progress(range(3), task_text="Counting to 3"):
        time.sleep(1)
