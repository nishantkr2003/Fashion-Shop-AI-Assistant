def format_result(
rows
):

    if not rows:

        return (
            "No results found."
        )

    output=[]

    for row in rows[:10]:

        block=[]

        for k,v in row.items():

            label=k.replace("_"," ").title()

            if(

                k
                ==
                "price"

            ):

                v=f"₹{v}"

            block.append(

f"{label}: {v}"

            )

        output.append(

"\n".join(
block
)

        )

    return (

"\n\n"

    ).join(
output
)