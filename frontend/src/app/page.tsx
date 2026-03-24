"use client";
import { useState, useEffect } from 'react';

const TENANT_ID = 1;

export default function Home() {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [runningAnalysis, setRunningAnalysis] = useState(false);
  
  const [form, setForm] = useState({
    product_name: 'Peak Milk 400g', 
    wholesale_cost: 3500, 
    desired_margin_percent: 15, 
    current_retail_price: 4500
  });

  const fetchInventory = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/inventory/${TENANT_ID}`);
      if (res.ok) {
         setInventory(await res.json());
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreateTenant = async () => {
     try {
       await fetch('http://localhost:8000/api/tenants/', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ name: "SME Vendor", contact_number: "+2347000000000" })
       });
     } catch (e) {
       console.error(e);
     }
  };

  useEffect(() => {
    handleCreateTenant().then(fetchInventory);
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await fetch(`http://localhost:8000/api/inventory/${TENANT_ID}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      fetchInventory();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const runAnalysis = async () => {
    setRunningAnalysis(true);
    try {
      const res = await fetch(`http://localhost:8000/api/analysis/run/${TENANT_ID}`, { method: 'POST' });
      const data = await res.json();
      alert(data.status);
    } catch (e) {
      console.error(e);
    }
    setRunningAnalysis(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-8 font-sans selection:bg-indigo-500/30">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="flex justify-between items-center pb-6 border-b border-gray-800">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">AI Price Guard</h1>
            <p className="text-gray-400 text-sm mt-1">Intelligent Margin Protection & Anomaly Alerting</p>
          </div>
          <button 
            onClick={runAnalysis}
            disabled={runningAnalysis}
            className={`px-6 py-2.5 rounded-full font-semibold transition-all duration-300 shadow-lg shadow-indigo-500/20 ${
              runningAnalysis ? 'bg-indigo-600/50 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 hover:-translate-y-0.5'
            }`}
          >
            {runningAnalysis ? 'Running Deep Analysis...' : 'Trigger Market Analysis'}
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 border border-gray-800 bg-gray-900/50 backdrop-blur-xl p-6 rounded-2xl shadow-xl">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <span className="p-1.5 bg-purple-500/20 text-purple-400 rounded-lg">📦</span>
              Add Inventory
            </h2>
            <form onSubmit={handleAdd} className="space-y-5">
              <div>
                <label className="block text-xs text-gray-400 uppercase tracking-wider mb-2 font-medium">Product Name</label>
                <input type="text" value={form.product_name} onChange={e => setForm({...form, product_name: e.target.value})} 
                  className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all" required/>
              </div>
              <div>
                <label className="block text-xs text-gray-400 uppercase tracking-wider mb-2 font-medium">Wholesale Cost (NGN)</label>
                <input type="number" value={form.wholesale_cost} onChange={e => setForm({...form, wholesale_cost: parseFloat(e.target.value)})} 
                  className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"/>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs text-gray-400 uppercase tracking-wider mb-2 font-medium">Margin (%)</label>
                  <input type="number" value={form.desired_margin_percent} onChange={e => setForm({...form, desired_margin_percent: parseFloat(e.target.value)})} 
                    className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"/>
                </div>
                <div>
                  <label className="block text-xs text-gray-400 uppercase tracking-wider mb-2 font-medium">Current Retail</label>
                  <input type="number" value={form.current_retail_price} onChange={e => setForm({...form, current_retail_price: parseFloat(e.target.value)})} 
                    className="w-full bg-gray-800/50 border border-gray-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"/>
                </div>
              </div>
              <button type="submit" disabled={loading} className="w-full bg-gray-800 hover:bg-gray-700 text-white py-3.5 rounded-xl font-medium transition-colors border border-gray-700 mt-4">
                {loading ? 'Adding...' : 'Save Product'}
              </button>
            </form>
          </div>

          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <span className="p-1.5 bg-emerald-500/20 text-emerald-400 rounded-lg">📊</span>
              Active Inventory
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {inventory.length === 0 ? (
                <div className="col-span-full py-12 text-center text-gray-500 border border-gray-800 border-dashed rounded-2xl">
                  No inventory added yet.
                </div>
              ) : (
                inventory.map((item, i) => (
                  <div key={i} className="group border border-gray-800 hover:border-gray-700 bg-gray-900/40 p-5 rounded-2xl transition-all hover:shadow-2xl hover:shadow-indigo-500/5">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="font-semibold text-lg truncate pr-4">{item.product_name}</h3>
                      <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        Active
                      </span>
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-500">Retail Price</span>
                        <span className="text-gray-200 font-medium">NGN {item.current_retail_price?.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-500">Target Margin</span>
                        <span className="text-indigo-400 font-medium">{item.desired_margin_percent}%</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
