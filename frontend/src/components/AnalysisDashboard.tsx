import React from 'react';
import { AnalysisResult, MedicalEntity } from '../services/api';
import SafetyAlert from './SafetyAlert';

interface Props {
    result: AnalysisResult;
}

const AnalysisDashboard: React.FC<Props> = ({ result }) => {
    return (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '15px', borderRadius: '8px', textAlign: 'left' }}>
            <h2>Analysis Complete</h2>
            <p><strong>Document ID:</strong> {result.document_id}</p>
            <p><strong>Detected Document Type:</strong> <span style={{ textTransform: 'capitalize', fontWeight: 'bold' }}>{result.document_type}</span></p>

            <div className="section" style={{ marginTop: '20px' }}>
                <h3>Summary</h3>
                <p>{result.summary}</p>
            </div>

            <div className="section" style={{ marginTop: '20px' }}>
                <h3>Key Findings</h3>
                <ul>
                    {result.key_findings.map((finding, index) => (
                        <li key={index}>{finding}</li>
                    ))}
                </ul>
            </div>

            <div className="section" style={{ marginTop: '20px' }}>
                <h3>Safety Assessment</h3>
                {result.safety_assessment.map((alert, index) => (
                    <SafetyAlert key={index} alert={alert} />
                ))}
            </div>

            <div className="section" style={{ marginTop: '20px' }}>
                <h3>Extracted Medical Entities</h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                    {result.extracted_entities.map((entity, index) => (
                        <EntityChip key={index} entity={entity} />
                    ))}
                </div>
            </div>
        </div>
    );
};

const EntityChip: React.FC<{ entity: MedicalEntity }> = ({ entity }) => {
    const colors: { [key: string]: string } = {
        medication: '#d0e8ff',
        diagnosis: '#ffe4d0',
        lab_test: '#d0ffd8',
        lab_value: '#e1d0ff',
        procedure: '#fffad0',
    };
    const chipStyle: React.CSSProperties = {
        backgroundColor: colors[entity.entity_type] || '#f0f0f0',
        padding: '5px 10px',
        borderRadius: '16px',
        border: '1px solid #ccc'
    };
    return (
        <div style={chipStyle}>
            <strong>{entity.entity_type}:</strong> {entity.entity_value}
            <span style={{ fontSize: '0.8em', color: '#555' }}> ({(entity.confidence_score * 100).toFixed(0)}%)</span>
        </div>
    );
};

export default AnalysisDashboard;```

### **`frontend/src/components/SafetyAlert.tsx`**

```typescript
import React from 'react';
import { SafetyAlert as SafetyAlertType } from '../services/api';

interface Props {
    alert: SafetyAlertType;
}

const SafetyAlert: React.FC<Props> = ({ alert }) => {
    const getSeverityStyles = (severity: string): React.CSSProperties => {
        switch (severity.toLowerCase()) {
            case 'critical':
            case 'high':
                return { borderLeft: '5px solid #d32f2f', backgroundColor: '#ffebee' };
            case 'major':
            case 'moderate':
                return { borderLeft: '5px solid #f57c00', backgroundColor: '#fff3e0' };
            case 'low':
                return { borderLeft: '5px solid #388e3c', backgroundColor: '#e8f5e9' };
            default:
                return { borderLeft: '5px solid #ccc', backgroundColor: '#f5f5f5' };
        }
    };

    const styles: React.CSSProperties = {
        padding: '15px',
        marginBottom: '10px',
        borderRadius: '4px',
        ...getSeverityStyles(alert.severity),
    };

    return (
        <div style={styles}>
            <h4 style={{ marginTop: 0, textTransform: 'capitalize' }}>
                {alert.title} ({alert.severity})
            </h4>
            <p style={{ margin: 0 }}>{alert.description}</p>
            {alert.action_required && <p style={{ marginTop: '10px', fontWeight: 'bold' }}>Action Required</p>}
        </div>
    );
};

export default SafetyAlert;