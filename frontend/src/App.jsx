import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Search, TrendingUp, Star, ThumbsUp, ThumbsDown, Award, AlertCircle, Loader } from 'lucide-react';

const AutoSentimentPlus = () => {
  const [products, setProducts] = useState(['', '']);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const analyzeProducts = async () => {
    const validProducts = products.filter(p => p.trim() !== '');

    if (validProducts.length < 2) {
      setError('Please enter at least 2 product names');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:5000/api/compare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ products: validProducts })
      });

      if (!response.ok) {
        throw new Error('Failed to analyze products');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError('Failed to connect to server. Make sure the backend is running on port 5000.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const addProduct = () => {
    if (products.length < 5) {
      setProducts([...products, '']);
    }
  };

  const updateProduct = (index, value) => {
    const newProducts = [...products];
    newProducts[index] = value;
    setProducts(newProducts);
  };

  const removeProduct = (index) => {
    if (products.length > 2) {
      const newProducts = products.filter((_, i) => i !== index);
      setProducts(newProducts);
    }
  };

  const hasValidResults = results && results.comparison.overall.some(p => p.score > 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-indigo-900 mb-2">🎯 AutoSentiment+</h1>
          <p className="text-gray-600 text-lg">Live Multilingual Product Comparison (Hindi & Marathi)</p>
          <p className="text-sm text-gray-500 mt-1">Real-time review scraping from Flipkart & Amazon</p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
            <Search className="mr-2" /> Enter Products to Compare
          </h2>

          <div className="space-y-3 mb-4">
            {products.map((product, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={product}
                  onChange={(e) => updateProduct(index, e.target.value)}
                  placeholder={`Product ${index + 1} (e.g., iPhone 15, Samsung S24, Nike Shoes, Sony TV)`}
                  className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none"
                />
                {products.length > 2 && (
                  <button
                    onClick={() => removeProduct(index)}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>

          <div className="flex gap-3">
            {products.length < 5 && (
              <button
                onClick={addProduct}
                className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 font-medium transition"
              >
                + Add Product
              </button>
            )}
            <button
              onClick={analyzeProducts}
              disabled={loading || products.filter(p => p.trim()).length < 2}
              className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center transition"
            >
              {loading ? (
                <>
                  <Loader className="mr-2 animate-spin" size={20} />
                  Analyzing Reviews...
                </>
              ) : (
                <>
                  Compare Products
                  <TrendingUp className="ml-2" size={20} />
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 flex items-start">
              <AlertCircle className="mr-2 mt-0.5 flex-shrink-0" size={20} />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <Loader className="animate-spin mx-auto mb-4 text-indigo-600" size={48} />
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Scraping Live Reviews...</h3>
            <p className="text-gray-600">Searching Flipkart and Amazon for Hindi & Marathi reviews</p>
            <p className="text-sm text-gray-500 mt-2">This may take 10-30 seconds</p>
          </div>
        )}

        {/* No Reviews Found */}
        {results && !hasValidResults && !loading && (
          <div className="bg-yellow-50 rounded-xl shadow-lg p-8 text-center border-2 border-yellow-400">
            <AlertCircle className="mx-auto mb-4 text-yellow-600" size={64} />
            <h3 className="text-2xl font-bold text-gray-800 mb-3">No Hindi/Marathi Reviews Found</h3>
            <p className="text-gray-700 mb-4">
              We couldn't find any Hindi or Marathi reviews for the products you searched.
            </p>
            <div className="bg-white rounded-lg p-4 mb-4">
              <h4 className="font-semibold text-gray-800 mb-2">Products searched:</h4>
              <ul className="text-gray-600">
                {products.filter(p => p.trim()).map((product, idx) => (
                  <li key={idx} className="mb-1">
                    • {product} {!results.comparison.reviewsFound[product] && '(No reviews)'}
                  </li>
                ))}
              </ul>
            </div>
            <p className="text-sm text-gray-600 mb-4">
              Try searching with different product names, or popular products like "iPhone 15", "Samsung Galaxy S24", "OnePlus 12"
            </p>
            <button
              onClick={() => {
                setResults(null);
                setProducts(['', '']);
              }}
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Results Section */}
        {results && hasValidResults && (
          <div className="space-y-6">
            {/* Winner Card */}
            {results.comparison.winner !== "No reviews found" && (
              <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl shadow-lg p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold mb-2 flex items-center">
                      <Award className="mr-2" size={32} />
                      Overall Winner
                    </h3>
                    <p className="text-3xl font-bold">{results.comparison.winner}</p>
                    <p className="text-lg mt-2">
                      Score: {results.comparison.overall.find(p => p.name === results.comparison.winner)?.score}/10
                    </p>
                  </div>
                  <Star size={80} fill="white" />
                </div>
              </div>
            )}

            {/* Radar Chart Comparison */}
            {results.comparison.radarData.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-2xl font-semibold text-gray-800 mb-4">📊 Aspect-wise Comparison</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <RadarChart data={results.comparison.radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="aspect" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    {products.filter((p, idx) => results.comparison.overall[idx]?.score > 0).map((product, idx) => {
                      const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#a0d8f1'];
                      return (
                        <Radar
                          key={idx}
                          name={product}
                          dataKey={product}
                          stroke={colors[idx]}
                          fill={colors[idx]}
                          fillOpacity={0.6}
                        />
                      );
                    })}
                    <Legend />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Bar Chart Comparison */}
            {results.comparison.aspects.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-2xl font-semibold text-gray-800 mb-4">📈 Feature-wise Sentiment Scores</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={results.comparison.aspects}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="aspect" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    {products.filter((p, idx) => results.comparison.overall[idx]?.score > 0).map((product, idx) => {
                      const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#a0d8f1'];
                      return (
                        <Bar key={idx} dataKey={product} fill={colors[idx]} />
                      );
                    })}
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Detailed Comparison */}
            <div className="grid md:grid-cols-2 gap-6">
              {products.filter(p => p.trim() && results.comparison.reviewsFound[p]).map((product, idx) => (
                <div key={idx} className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-4 border-b pb-2">{product}</h3>

                  <div className="mb-4">
                    <h4 className="font-semibold text-green-600 mb-2 flex items-center">
                      <ThumbsUp className="mr-2" size={18} /> Strengths
                    </h4>
                    <ul className="space-y-1">
                      {results.comparison.strengths[product]?.map((strength, i) => (
                        <li key={i} className="text-gray-700">• {strength}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-red-600 mb-2 flex items-center">
                      <ThumbsDown className="mr-2" size={18} /> Weaknesses
                    </h4>
                    <ul className="space-y-1">
                      {results.comparison.weaknesses[product]?.map((weakness, i) => (
                        <li key={i} className="text-gray-700">• {weakness}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Sample Reviews</h4>
                    <div className="space-y-2">
                      {results.comparison.reviews[product]?.map((review, i) => (
                        <div key={i} className="bg-gray-50 p-3 rounded-lg">
                          <div className="flex items-center justify-between mb-1">
                            <div className="flex">
                              {[...Array(5)].map((_, starIdx) => (
                                <Star
                                  key={starIdx}
                                  size={14}
                                  fill={starIdx < review.rating ? '#fbbf24' : 'none'}
                                  stroke={starIdx < review.rating ? '#fbbf24' : '#d1d5db'}
                                />
                              ))}
                            </div>
                            <span className="text-xs text-gray-500 capitalize">{review.language}</span>
                          </div>
                          <p className="text-sm text-gray-700 mb-1">{review.text}</p>
                          <span className="inline-block px-2 py-1 bg-indigo-100 text-indigo-700 text-xs rounded">
                            {review.aspect}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Info Section */}
        {!results && !loading && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-center">How it works</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <div className="flex items-start">
                  <div className="bg-indigo-100 rounded-full p-2 mr-3">
                    <Search size={20} className="text-indigo-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-800">Real-time Scraping</h4>
                    <p className="text-gray-600 text-sm">Live scraping from Flipkart & Amazon for latest reviews</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="bg-green-100 rounded-full p-2 mr-3">
                    <TrendingUp size={20} className="text-green-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-800">AI-Powered Analysis</h4>
                    <p className="text-gray-600 text-sm">XLM-RoBERTa model trained on Hindi & Marathi reviews</p>
                  </div>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-start">
                  <div className="bg-purple-100 rounded-full p-2 mr-3">
                    <Award size={20} className="text-purple-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-800">Aspect-Based Comparison</h4>
                    <p className="text-gray-600 text-sm">Compare products across multiple aspects and features</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="bg-orange-100 rounded-full p-2 mr-3">
                    <Star size={20} className="text-orange-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-800">Multilingual Support</h4>
                    <p className="text-gray-600 text-sm">Analyzes Hindi and Marathi reviews with high accuracy</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-700 text-center">
                <strong>Note:</strong> Works for any product category - Electronics, Clothing, Appliances, Food, and more!
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AutoSentimentPlus;