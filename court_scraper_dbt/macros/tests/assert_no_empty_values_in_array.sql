{% test no_empty_arrays(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }}
WHERE
    ARRAY_LENGTH({{ column_name }}) = 0  -- Ensure array is not empty

{% endtest %}

{% test no_empty_values_in_array(model, column_name) %}

SELECT value
FROM (
    SELECT UNNEST({{ column_name }}) AS value
    FROM {{ model }}
) subquery
WHERE TRIM(value) = ''

{% endtest %}
