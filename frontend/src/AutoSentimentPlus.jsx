import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Search, TrendingUp, Star, ThumbsUp, ThumbsDown, Award } from 'lucide-react';

const AutoSentimentPlus = () => {
  const [products, setProducts] = useState(['', '']);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  // Simulated analysis function (in real app, this calls your backend API)
  const analyzeProducts = () => {
    setLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      // Mock data - replace with actual API call
      const mockResults = {
        products: products.filter(p => p.trim() !== ''),
        comparison: {
          overall: [
            { name: products[0], score: 8.2, sentiment: 'positive' },
            { name: products[1], score: 7.5, sentiment: 'positive' }
          ],
          aspects: [
            { aspect: 'Camera', [products[0]]: 78, [products[1]]: 65 },
            { aspect: 'Battery', [products[0]]: 68, [products[1]]: 82 },
            { aspect: 'Performance', [products[0]]: 85, [products[1]]: 73 },
            { aspect: 'Display', [products[0]]: 80, [products[1]]: 78 },
            { aspect: 'Value', [products[0]]: 71, [products[1]]: 69 },
            { aspect: 'Build Quality', [products[0]]: 75, [products[1]]: 70 }
          ],
          radarData: [
            { aspect: 'Camera', [products[0]]: 78, [products[1]]: 65, fullMark: 100 },
            { aspect: 'Battery', [products[0]]: 68, [products[1]]: 82, fullMark: 100 },
            { aspect: 'Performance', [products[0]]: 85, [products[1]]: 73, fullMark: 100 },
            { aspect: 'Display', [products[0]]: 80, [products[1]]: 78, fullMark: 100 },
            { aspect: 'Value', [products[0]]: 71, [products[1]]: 69, fullMark: 100 },
            { aspect: 'Build', [products[0]]: 75, [products[1]]: 70, fullMark: 100 }
          ],
          reviews: {
            [products[0]]: [
              { text: 'कैमरा बहुत बढ़िया है, फोटो क्वालिटी शानदार', rating: 5, aspect: 'Camera' },
              { text: 'बैटरी बैकअप थोड़ा कम है', rating: 3, aspect: 'Battery' },
              { text: 'परफॉर्मेंस एकदम जबरदस्त, कोई लैग नहीं', rating: 5, aspect: 'Performance' }
            ],
            [products[1]]: [
              { text: 'बैटरी लाइफ बहुत अच्छी है, पूरे दिन चलती है', rating: 5, aspect: 'Battery' },
              { text: 'कैमरा ठीक है पर low light में कमजोर', rating: 3, aspect: 'Camera' },
              { text: 'पैसे के हिसाब से बढ़िया प्रोडक्ट', rating: 4, aspect: 'Value' }
            ]
          },
          winner: products[0],
          strengths: {
            [products[0]]: ['Camera Quality', 'Performance', 'Display'],
            [products[1]]: ['Battery Life', 'Value for Money']
          },
          weaknesses: {
            [products[0]]: ['Battery Backup', 'Price'],
            [products[1]]: ['Camera in Low Light', 'Performance']
          }
        }
      };

      setResults(mockResults);
      setLoading(false);
    }, 1500);
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-indigo-900 mb-2">AutoSentiment+</h1>
          <p className="text-gray-600 text-lg">Multilingual Product Comparison System (Hindi & Marathi)</p>
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
                  placeholder={`Product ${index + 1} name (e.g., iPhone 15, Samsung S24)`}
                  className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none"
                />
                {products.length > 2 && (
                  <button
                    onClick={() => removeProduct(index)}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
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
                className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 font-medium"
              >
                + Add Product
              </button>
            )}
            <button
              onClick={analyzeProducts}
              disabled={loading || products.filter(p => p.trim()).length < 2}
              className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
            >
              {loading ? 'Analyzing...' : 'Compare Products'}
              {!loading && <TrendingUp className="ml-2" size={20} />}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {results && (
          <div className="space-y-6">
            {/* Winner Card */}
            <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl shadow-lg p-6 text-white">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-2xl font-bold mb-2 flex items-center">
                    <Award className="mr-2" size={32} />
                    Overall Winner
                  </h3>
                  <p className="text-3xl font-bold">{results.comparison.winner}</p>
                  <p className="text-lg mt-2">Score: {results.comparison.overall[0].score}/10</p>
                </div>
                <Star size={80} fill="white" />
              </div>
            </div>

            {/* Radar Chart Comparison */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">Aspect-wise Comparison</h3>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={results.comparison.radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="aspect" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name={products[0]} dataKey={products[0]} stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                  <Radar name={products[1]} dataKey={products[1]} stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                  <Legend />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Bar Chart Comparison */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">Feature-wise Sentiment Scores</h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={results.comparison.aspects}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="aspect" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey={products[0]} fill="#8884d8" />
                  <Bar dataKey={products[1]} fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Detailed Comparison */}
            <div className="grid md:grid-cols-2 gap-6">
              {products.filter(p => p.trim()).map((product, idx) => (
                <div key={idx} className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-4 border-b pb-2">{product}</h3>

                  <div className="mb-4">
                    <h4 className="font-semibold text-green-600 mb-2 flex items-center">
                      <ThumbsUp className="mr-2" size={18} /> Strengths
                    </h4>
                    <ul className="space-y-1">
                      {results.comparison.strengths[product].map((strength, i) => (
                        <li key={i} className="text-gray-700">• {strength}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-red-600 mb-2 flex items-center">
                      <ThumbsDown className="mr-2" size={18} /> Weaknesses
                    </h4>
                    <ul className="space-y-1">
                      {results.comparison.weaknesses[product].map((weakness, i) => (
                        <li key={i} className="text-gray-700">• {weakness}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Sample Reviews</h4>
                    <div className="space-y-2">
                      {results.comparison.reviews[product].map((review, i) => (
                        <div key={i} className="bg-gray-50 p-3 rounded-lg">
                          <div className="flex items-center mb-1">
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
                            <span className="ml-2 text-xs text-gray-500">{review.aspect}</span>
                          </div>
                          <p className="text-sm text-gray-700">{review.text}</p>
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
        {!results && (
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">How it works</h3>
            <p className="text-gray-600 mb-2">1. Enter 2 or more product names</p>
            <p className="text-gray-600 mb-2">2. Our AI analyzes Hindi & Marathi reviews</p>
            <p className="text-gray-600 mb-2">3. Get detailed aspect-based comparison</p>
            <p className="text-gray-600">4. Make informed purchase decisions!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AutoSentimentPlus;