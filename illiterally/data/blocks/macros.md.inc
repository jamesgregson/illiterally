{% macro ref(slug) %}
    {%- set __blk = block(slug) -%}
    {%- if __blk -%}
        {%- if __blk.is_rendered -%}
            [{{__blk.name}}]({{__blk.rendered_into}}#{{__blk.slug}})
        {%- else -%}
            <font color="red">MissingBlock({{__blk.slug}})</font>
        {%- endif -%}
    {%- else -%}
        <font color="red">InvalidSlug({{slug}})</font>
    {%- endif -%}
{% endmacro %}