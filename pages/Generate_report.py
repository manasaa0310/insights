import streamlit as st
from matplotlib.backends.backend_pdf import PdfPages
from io import BytesIO
import matplotlib.pyplot as plt

st.title("🧾 Generate Report")

if 'report_figures' in st.session_state and st.session_state['report_figures']:
    pdf_buffer = BytesIO()

    with PdfPages(pdf_buffer) as pdf:
        for plotly_fig in st.session_state['report_figures']:
            # Plotly figure to matplotlib fallback via PNG workaround
            try:
                img_bytes = plotly_fig.to_image(format="png", engine="kaleido")  # this fails on cloud
            except Exception:
                st.warning("📷 Image export not supported on Streamlit Cloud. Try generating this report locally.")
                st.stop()

            # Convert image bytes to matplotlib figure
            image = plt.imread(BytesIO(img_bytes), format='png')
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(image)
            ax.axis('off')
            pdf.savefig(fig)
            plt.close(fig)

    st.success("✅ PDF Report Generated!")

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_buffer.getvalue(),
        file_name="Data_Insights_Report.pdf",
        mime="application/pdf"
    )
else:
    st.warning("No visualizations available. Go to the Dashboard page and upload data.")
