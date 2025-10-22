import React from "react";


export default function ResumeAnalysis({ result }) {
  if (!result) return null;

  const { skill_match_score, matched_by_category, missing_by_category } = result;

  return (
    <div className="p-6 space-y-6">
      {/* Overall Score */}
      <div className="mb-4">
        <h2 className="text-2xl font-bold mb-2">Skill Match Score</h2>
        <div className="w-full bg-gray-200 rounded-full h-6">
          <div
            className="bg-green-500 h-6 rounded-full text-center text-white font-bold"
            style={{ width: `${skill_match_score}%` }}
          >
            {skill_match_score}%
          </div>
        </div>
      </div>

      {/* Skills by Category */}
      {Object.keys(matched_by_category).map((category) => (
        <div key={category} className="border p-4 rounded-lg shadow-sm">
          <h3 className="text-xl font-semibold mb-2">{category}</h3>
          <div className="">
            {/* Matched Skills */}
            {matched_by_category[category].map((skill) => (
              <p
                key={skill}
                className="px-2 py-1 bg-green-200 text-green-800 rounded-full text-sm"
              >
                {skill}
              </p>
            ))}

            {/* Missing Skills */}
            {missing_by_category[category].map((skill) => (
              <p
                key={skill}
                className="px-2 py-1 bg-red-200 text-red-800 rounded-full text-sm"
              >
                {skill}
              </p>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
