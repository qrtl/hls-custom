This module does the following:

* Adds the functionality of defaulting the secondary unit in the detailed operation
  lines from stock.move.
* Adjust the move detail view to hide the secondary unit column in the operation lines,
  since the default value presentation of the field has an issue (it is not visible on
  UI for some reason until the line is saved) and the field is not expected to be
  updated at the line level.
