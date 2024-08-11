import fitz  
import io
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if 'sources' not in st.session_state:
    st.session_state.sources = []  
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

if uploaded_file is not None:
    try:
        file_content = uploaded_file.read()

        doc = fitz.open(stream=io.BytesIO(file_content), filetype="pdf")
        st.write(f"PDF opened successfully: {doc.page_count} pages found.")

        def find_pages_with_excerpts(doc, excerpts):
            pages_with_excerpts = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                for excerpt in excerpts:
                    text_instances = page.search_for(excerpt)
                    if text_instances:
                        pages_with_excerpts.append(page_num + 1)
                        break
            return pages_with_excerpts if pages_with_excerpts else [1]

        def get_highlight_info(doc, excerpts):
            annotations = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                for excerpt in excerpts:
                    text_instances = page.search_for(excerpt)
                    if text_instances:
                        for inst in text_instances:
                            annotations.append({
                                "page": page_num + 1,
                                "x": inst.x0,
                                "y": inst.y0,
                                "width": inst.x1 - inst.x0,
                                "height": inst.y1 - inst.y0,
                                "color": "red",
                            })
            return annotations

        pages_with_excerpts = find_pages_with_excerpts(doc, st.session_state.sources)
        annotations = get_highlight_info(doc, st.session_state.sources)

        if annotations:
            first_page_with_excerpts = min(ann["page"] for ann in annotations)
        else:
            first_page_with_excerpts = st.session_state.current_page + 1

        pdf_viewer(
            file_content,
            width=700,
            height=800,
            annotations=annotations,
            pages_to_render=[first_page_with_excerpts],
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a PDF file to proceed.")





