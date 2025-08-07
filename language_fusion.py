# language_fusion.py

def fuse_with_llm(capability, anchor_cluster, llm):
    anchor_texts = [a["expression"] for a in anchor_cluster]
    prompt = f"Given the symbolic pattern:\n" + "\n".join(anchor_texts)
    prompt += f"\n\nCan you perform a {capability} based on this?"

    response = llm(
        f"### Question:\n{prompt}\n\n### Answer:\n",
        max_tokens=200,
        stop=["###"],
        echo=False,
        temperature=0.7
    )
    return response["choices"][0]["text"].strip()
