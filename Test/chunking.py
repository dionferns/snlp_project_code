# import json

# # Load the JSON document
# with open("2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement.json", "r") as file:
#     document = json.load(file)

# chunks = []

# # Loop through sections
# for section in document["sections"]:
#     section_id = section["section_id"]
#     section_title = section["title"]
    
#     # If the section has subsections, create individual chunks
#     if "subsections" in section:
#         for subsection in section["subsections"]:
#             chunk = {
#                 "section_id": section_id,
#                 "subsection_id": subsection["subsection_id"],
#                 "title": f"{section_title} - {subsection['title']}",
#                 "text": subsection["text"]
#             }
#             chunks.append(chunk)
#     else:
#         # If no subsections, create a chunk for the section itself
#         chunk = {
#             "section_id": section_id,
#             "title": section_title,
#             "text": section.get("text", "")  # Some sections may not have direct text
#         }
#         chunks.append(chunk)

# # Include appendices if present
# if "appendices" in document:
#     for appendix in document["appendices"]:
#         chunk = {
#             "section_id": f"Appendix {appendix['appendix_id']}",
#             "title": appendix["title"],
#             "text": appendix["text"]
#         }
#         chunks.append(chunk)

# # Print sample chunks to verify the structure
# for chunk in chunks[:5]:  # Print first 5 chunks
#     print(json.dumps(chunk, indent=2))

# # Save chunks as a new JSON file
# with open("chunked_co_branding_agreement.json", "w") as output_file:
#     json.dump(chunks, output_file, indent=2)

# print("Chunking completed and saved as chunked_co_branding_agreement.json.")



import json

# Load the JSON document
with open("2ThemartComInc_19990826_10-12G_EX-10.10_6700288_EX-10.10_Co-Branding Agreement_ Agency Agreement.json", "r") as file:
    document = json.load(file)

chunks = []

# Loop through sections
for section in document["sections"]:
    section_id = section["section_id"]
    section_title = section["title"]
    
    # If the section has definitions, process them separately
    if "definitions" in section:
        for definition in section["definitions"]:
            chunk = {
                "section_id": section_id,
                "title": f"{section_title} - Definition of {definition['term']}",
                "text": definition["definition"]
            }
            chunks.append(chunk)

    # If the section has subsections, process them
    if "subsections" in section:
        for subsection in section["subsections"]:
            chunk = {
                "section_id": section_id,
                "subsection_id": subsection["subsection_id"],
                "title": f"{section_title} - {subsection['title']}",
                "text": subsection["text"]
            }
            chunks.append(chunk)
    elif "text" in section:  # If section has text but no subsections
        chunk = {
            "section_id": section_id,
            "title": section_title,
            "text": section["text"]
        }
        chunks.append(chunk)

# Include appendices if present
if "appendices" in document:
    for appendix in document["appendices"]:
        chunk = {
            "section_id": f"Appendix {appendix['appendix_id']}",
            "title": appendix["title"],
            "text": appendix["text"]
        }
        chunks.append(chunk)

# Print sample chunks to verify the structure
for chunk in chunks[:5]:  # Print first 5 chunks
    print(json.dumps(chunk, indent=2))

# Save chunks as a new JSON file
with open("chunked_co_branding_agreement.json", "w") as output_file:
    json.dump(chunks, output_file, indent=2)

print("Chunking completed and saved as chunked_co_branding_agreement.json.")
