# 🏛️ Indian Cultural Heritage Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indian-cultural-heritage-explorer.streamlit.app/)

An interactive web application that explores and visualizes India's rich cultural heritage through data analytics, machine learning, and interactive visualizations. This application provides comprehensive insights into India's monuments, traditions, art forms, and cultural diversity.

## 🚀 Live Demo

**[Access the Application](https://indian-cultural-heritage-explorer.streamlit.app/)**

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Methodology](#-methodology)
- [Impact & Metrics](#-impact--metrics)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🗺️ Interactive Heritage Mapping
- **Geographic Visualization**: Interactive maps showing heritage sites across India
- **Site Details**: Comprehensive information about monuments, temples, and cultural sites
- **Location-based Search**: Find heritage sites by state, region, or proximity

### 📊 Data Analytics & Insights
- **Statistical Analysis**: Comprehensive statistics on India's cultural heritage
- **Trend Analysis**: Historical trends in heritage preservation and tourism
- **Comparative Studies**: Regional comparisons of cultural diversity

### 🤖 AI-Powered Features
- **Heritage Chatbot**: Ask questions about Indian culture and get AI-powered responses
- **Smart Recommendations**: Personalized heritage site recommendations
- **Cultural Context**: AI-generated explanations of cultural significance

### 📈 Visualization Dashboard
- **Interactive Charts**: Dynamic visualizations using Plotly
- **Statistical Dashboards**: Heritage site statistics and analytics
- **Trend Monitoring**: Track heritage preservation efforts

### 📄 Report Generation
- **Custom Reports**: Generate detailed PDF reports on specific heritage topics
- **Data Export**: Export visualizations and data for research purposes
- **Documentation**: Comprehensive heritage site documentation

## 🛠️ Tech Stack

### **Frontend & Framework**
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) **Streamlit 1.38.0** - Web application framework
- ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) **Interactive UI Components**

### **Data Processing & Analysis**
- ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) **Pandas 2.2.2** - Data manipulation and analysis
- ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) **NumPy 1.26.4** - Numerical computations
- ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) **Scikit-learn 1.5.2** - Machine learning algorithms

### **Data Visualization**
- ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) **Plotly 5.24.0** - Interactive visualizations
- ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white) **Matplotlib 3.9.2** - Static plotting
- ![Seaborn](https://img.shields.io/badge/Seaborn-blue?style=flat&logo=python&logoColor=white) **Seaborn 0.13.2** - Statistical visualizations
- ![Folium](https://img.shields.io/badge/Folium-77B829?style=flat&logo=folium&logoColor=white) **Folium 0.17.0** - Interactive maps

### **Database & Cloud**
- ![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat&logo=snowflake&logoColor=white) **Snowflake** - Cloud data warehouse
- ![PyArrow](https://img.shields.io/badge/PyArrow-4285F4?style=flat&logo=apache&logoColor=white) **PyArrow 17.0.0** - Columnar data processing

### **AI & Machine Learning**
- ![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=flat&logo=google&logoColor=white) **Google Generative AI 0.8.3** - AI-powered features
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.11+** - Core programming language

### **Document Processing & Security**
- ![ReportLab](https://img.shields.io/badge/ReportLab-orange?style=flat&logo=python&logoColor=white) **ReportLab 4.2.2** - PDF generation
- ![Pillow](https://img.shields.io/badge/Pillow-blue?style=flat&logo=python&logoColor=white) **Pillow 10.4.0** - Image processing
- ![OpenSSL](https://img.shields.io/badge/OpenSSL-721412?style=flat&logo=openssl&logoColor=white) **pyOpenSSL 24.0.0+** - Security protocols

## 🏗️ Architecture

-![Flow of Project](https://raw.githubusercontent.com/SravikaPadakanti/Indian-Cultural-Heritage-Explorer/main/System_architecture.png)

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- Git

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/indian-cultural-heritage-explorer.git
   cd indian-cultural-heritage-explorer
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   echo "SNOWFLAKE_USER=your_snowflake_user" >> .env
   echo "SNOWFLAKE_PASSWORD=your_snowflake_password" >> .env
   echo "SNOWFLAKE_ACCOUNT=your_snowflake_account" >> .env
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

### Deploy to Streamlit Cloud

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your forked repository
5. Set main file path: `app.py`
6. Add your environment variables in the secrets management
7. Click "Deploy"

## 📖 Usage

### 🏛️ Exploring Heritage Sites
1. **Navigate to the Map Section**: View interactive maps of heritage sites
2. **Filter by Region**: Use dropdown menus to filter sites by state or region
3. **Click on Markers**: Get detailed information about specific heritage sites
4. **View Statistics**: Access comprehensive data about each location

### 📊 Analytics Dashboard
1. **Statistical Overview**: View key metrics about India's cultural heritage
2. **Trend Analysis**: Analyze historical data and trends
3. **Comparative Studies**: Compare different regions or time periods
4. **Custom Visualizations**: Create custom charts and graphs

### 🤖 AI-Powered Features
1. **Heritage Chatbot**: Ask questions about Indian culture and history
2. **Smart Recommendations**: Get personalized heritage site suggestions
3. **Cultural Insights**: Receive AI-generated explanations and context

### 📄 Report Generation
1. **Select Data**: Choose specific heritage topics or regions
2. **Customize Report**: Set parameters and visualization preferences
3. **Generate PDF**: Create comprehensive reports for research or presentation
4. **Export Data**: Download data in various formats (CSV, JSON, PDF)

## 🔬 Methodology

### Data Collection & Processing
- **Primary Sources**: Archaeological Survey of India (ASI), UNESCO World Heritage Sites
- **Secondary Sources**: Tourism data, historical records, cultural documentation
- **Data Cleaning**: Automated preprocessing using Pandas and NumPy
- **Quality Assurance**: Multi-stage validation and verification processes

### Machine Learning Approach
- **Clustering Analysis**: Group similar heritage sites using scikit-learn
- **Recommendation Engine**: Content-based filtering for personalized suggestions
- **Predictive Analytics**: Tourism trend forecasting and heritage preservation insights
- **Natural Language Processing**: AI-powered cultural context generation

### Visualization Strategy
- **Interactive Design**: User-centric interface with dynamic visualizations
- **Geographic Mapping**: Spatial analysis using Folium and geographic libraries
- **Statistical Representation**: Multi-dimensional data visualization with Plotly
- **Responsive Layout**: Mobile-friendly design with Streamlit components

## 📈 Impact & Metrics

### Educational Impact
- 📚 **Knowledge Dissemination**: Making cultural heritage accessible to global audiences
- 🎓 **Research Support**: Providing tools for academic and cultural research
- 👥 **Community Engagement**: Connecting people with their cultural roots

### Technical Achievements
- ⚡ **Performance**: Sub-second query response times
- 🔄 **Scalability**: Handles concurrent users efficiently
- 📱 **Accessibility**: Mobile-responsive design
- 🌐 **Global Reach**: Accessible worldwide through cloud deployment

### User Engagement Metrics
- 📊 **Active Users**: Tracking daily and monthly active users
- ⏱️ **Session Duration**: Average engagement time per session
- 🔍 **Feature Usage**: Most popular features and user pathways
- 📈 **Growth Rate**: User acquisition and retention metrics

### Cultural Preservation Goals
- 🏛️ **Site Documentation**: Comprehensive digital archiving
- 📍 **Location Mapping**: Precise geographic documentation
- 🔍 **Research Facilitation**: Supporting academic and cultural studies
- 🌟 **Awareness Building**: Promoting cultural heritage appreciation

## 📸 Screenshots

### Main Dashboard
![Dashboard](https://via.placeholder.com/800x400/4285F4/FFFFFF?text=Main+Dashboard)
*Interactive dashboard showing heritage site statistics and key metrics*

### Heritage Map
![Heritage Map](https://via.placeholder.com/800x400/34A853/FFFFFF?text=Interactive+Heritage+Map)
*Geographic visualization of heritage sites across India with filtering options*

### Analytics Section
![Analytics](https://via.placeholder.com/800x400/EA4335/FFFFFF?text=Data+Analytics+Dashboard)
*Comprehensive analytics dashboard with charts, trends, and insights*

### AI Chatbot
![AI Chatbot](https://via.placeholder.com/800x400/FBBC04/FFFFFF?text=AI-Powered+Heritage+Chatbot)
*AI-powered chatbot providing cultural heritage information and recommendations*

## 🤝 Contributing

We welcome contributions to enhance the Indian Cultural Heritage Explorer! Here's how you can contribute:

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Areas for Contribution
- 🗺️ **New Heritage Sites**: Add more heritage locations and cultural sites
- 🎨 **UI/UX Improvements**: Enhance user interface and experience
- 📊 **Data Visualizations**: Create new charts and interactive elements
- 🤖 **AI Features**: Improve AI-powered recommendations and insights
- 🌐 **Localization**: Add support for regional languages
- 📱 **Mobile Optimization**: Enhance mobile user experience

## 📋 Requirements

```text
streamlit==1.38.0; python_version >= '3.11' and python_version < '3.12'
pandas==2.2.2; python_version >= '3.11' and python_version < '3.12'
numpy==1.26.4; python_version >= '3.11' and python_version < '3.12'
plotly==5.24.0; python_version >= '3.11' and python_version < '3.12'
folium==0.17.0; python_version >= '3.11' and python_version < '3.12'
streamlit-folium==0.22.0; python_version >= '3.11' and python_version < '3.12'
snowflake-snowpark-python; python_version >= '3.11' and python_version < '3.12'
scikit-learn==1.5.2; python_version >= '3.11' and python_version < '3.12'
reportlab==4.2.2; python_version >= '3.11' and python_version < '3.12'
requests==2.32.3; python_version >= '3.11' and python_version < '3.12'
Pillow==10.4.0; python_version >= '3.11' and python_version < '3.12'
matplotlib==3.9.2; python_version >= '3.11' and python_version < '3.12'
seaborn==0.13.2; python_version >= '3.11' and python_version < '3.12'
branca==0.8.0; python_version >= '3.11' and python_version < '3.12'
google-generativeai==0.8.3; python_version >= '3.11' and python_version < '3.12'
pyarrow==17.0.0; python_version >= '3.11' and python_version < '3.12'
pyOpenSSL>=24.0.0; python_version >= '3.11' and python_version < '3.12'
cryptography>=41.0.0; python_version >= '3.11' and python_version < '3.12'
python-dotenv; python_version >= '3.11' and python_version < '3.12'
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Archaeological Survey of India (ASI)** for heritage site data
- **UNESCO** for World Heritage Site information
- **Streamlit Community** for the amazing framework
- **Google AI** for generative AI capabilities
- **Open Source Contributors** who made this project possible

## 📞 Contact & Support

- 🌐 **Live App**: [indian-cultural-heritage-explorer.streamlit.app](https://indian-cultural-heritage-explorer.streamlit.app/)
- 📧 **Email**: padakantisravikaa@gmail.com
- 💼 **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/sravika-padakanti/)
- 🐙 **GitHub**: [Your GitHub Profile](https://github.com/SravikaPadakanti/)

---

<div align="center">

**Built with ❤️ for preserving and celebrating India's rich cultural heritage**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Powered%20by-Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Google AI](https://img.shields.io/badge/AI%20by-Google-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google)

</div>
