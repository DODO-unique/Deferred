it is tricky but as said in other docs there are somethings you must remember:

1. ChunkedIteratorResult is of the type Model. So say the cir is from Users model, then you can hint it as `cir_obj : Users`
2. when using Join you have to use it like `.join(Parent, Children.fk_column_name == Parent.id)`
3. The use of the join is so you can then just find in children's table using filters from other columns in Parent... complicated but you will get the feel of it once you touch it.