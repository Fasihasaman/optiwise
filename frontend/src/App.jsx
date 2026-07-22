import { BrowserRouter, Routes, Route } from "react-router-dom";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import AskData from "./pages/AskData";
import Layout from "./components/Layout";
import DatasetExplorer from "./pages/DatasetExplorer";

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Upload />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/ask" element={<AskData />} />
          <Route
            path="/explorer"
            element={<DatasetExplorer />}
          />

        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;