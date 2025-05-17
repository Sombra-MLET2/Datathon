import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Paper, 
  Button, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Grid,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Chip,
  Stack,
  Breadcrumbs,
  ToggleButtonGroup,
  ToggleButton,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Tooltip
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Person as PersonIcon,
  Work as WorkIcon,
  ExitToApp as LogoutIcon,
  ArrowBack as ArrowBackIcon,
  LocationOn as LocationIcon,
  Business as BusinessIcon,
  CalendarToday as CalendarIcon,
  Assignment as AssignmentIcon,
  Search as SearchIcon,
  ExpandMore as ExpandMoreIcon,
  Visibility as VisibilityIcon,
  Insights,
  Psychology as PsychologyIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useParams, Link } from 'react-router-dom';
import axios from 'axios';

const JobVacancyDetailPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { id } = useParams();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [vacancy, setVacancy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [topCandidatesCount, setTopCandidatesCount] = useState(10);
  const [searchingCandidates, setSearchingCandidates] = useState(false);
  const [topCandidates, setTopCandidates] = useState([]);
  const [searchError, setSearchError] = useState('');
  const [searchSuccess, setSearchSuccess] = useState(false);
  const [foundCount, setFoundCount] = useState(0);
  const [offerChances, setOfferChances] = useState({});
  const [loadingOfferChances, setLoadingOfferChances] = useState({});
  const [cvAnalysis, setCvAnalysis] = useState({});
  const [loadingCvAnalysis, setLoadingCvAnalysis] = useState({});

  useEffect(() => {
    const fetchVacancyDetails = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/job-vacancies/${id}`);
        setVacancy(response.data);
        setError('');
      } catch (err) {
        console.error('Error fetching vacancy details:', err);
        setError('Failed to load job vacancy details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchVacancyDetails();
  }, [id]);

  const handleTopCandidatesCountChange = (event, newCount) => {
    if (newCount !== null) {
      setTopCandidatesCount(newCount);
    }
  };

  const searchTopCandidates = async () => {
    if (!vacancy) return;
    
    try {
      setSearchingCandidates(true);
      setSearchError('');
      setTopCandidates([]);
      setSearchSuccess(false);
      setFoundCount(0);
      
      // Determine job description to use
      const jobDescription = vacancy.principais_atividades || vacancy.competencia_tecnicas_e_comportamentais || '';
      
      if (!jobDescription) {
        setSearchError('No job description available to search candidates.');
        setSearchingCandidates(false);
        return;
      }
      
      const response = await axios.post('/api/candidates/search', {
        top_candidates: topCandidatesCount,
        job_description: jobDescription
      });
      
      if (response.data.success) {
        setSearchSuccess(true);
        setFoundCount(response.data.found);
        
        // Sort candidates by similarity (highest to lowest)
        const sortedCandidates = [...(response.data.candidates || [])].sort((a, b) => 
          (b.similarity || 0) - (a.similarity || 0)
        );
        
        setTopCandidates(sortedCandidates);
      } else {
        setSearchError('Search completed but no candidates were found.');
      }
    } catch (err) {
      console.error('Error searching top candidates:', err);
      setSearchError('Failed to search for top candidates. Please try again later.');
    } finally {
      setSearchingCandidates(false);
    }
  };

  const getOfferChances = async (candidateId, professionalCode) => {
    if (!vacancy || !candidateId) return;
    
    try {
      setLoadingOfferChances(prev => ({ ...prev, [candidateId]: true }));
      
      const response = await axios.get(`/api/job-vacancies/${id}/offer-inference/${professionalCode}`);
      
      setOfferChances(prev => ({ 
        ...prev, 
        [candidateId]: response.data.acceptance_probability 
      }));
    } catch (err) {
      console.error('Error getting offer chances:', err);
      // Set a negative value to indicate error
      setOfferChances(prev => ({ ...prev, [candidateId]: -1 }));
    } finally {
      setLoadingOfferChances(prev => ({ ...prev, [candidateId]: false }));
    }
  };

  const analyzeCandidateCV = async (candidateId, similarity) => {
    if (!vacancy || !candidateId) return;
    
    try {
      setLoadingCvAnalysis(prev => ({ ...prev, [candidateId]: true }));
      
      const acceptanceProbability = offerChances[candidateId] || 0;
      
      const response = await axios.post(`/api/job-vacancies/${id}/analyze-cv`, {
        candidate_id: candidateId,
        similarity: similarity / 100,
        acceptance_probability: acceptanceProbability
      });
      
      setCvAnalysis(prev => ({ 
        ...prev, 
        [candidateId]: response.data.analysis 
      }));
    } catch (err) {
      console.error('Error analyzing CV:', err);
      setCvAnalysis(prev => ({
        ...prev, 
        [candidateId]: "Erro na análise do CV. Por favor, tente novamente mais tarde."
      }));
    } finally {
      setLoadingCvAnalysis(prev => ({ ...prev, [candidateId]: false }));
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const navigateTo = (path) => {
    navigate(path);
  };

  // Function to get color based on similarity score
  const getSimilarityColor = (similarity) => {
    // Convert similarity to a value between 0 and 1
    const normalizedScore = similarity / 100;
    
    // Green for high scores, transitioning to blue for lower scores
    if (normalizedScore > 0.8) return '#4caf50'; // Green
    if (normalizedScore > 0.6) return '#81c784'; // Light Green
    if (normalizedScore > 0.4) return '#64b5f6'; // Light Blue
    if (normalizedScore > 0.2) return '#2196f3'; // Blue
    return '#1976d2'; // Dark Blue
  };

  // Function to get color based on acceptance probability
  const getAcceptanceProbabilityColor = (probability) => {
    if (probability > 0.8) return '#4caf50'; // Green
    if (probability > 0.6) return '#81c784'; // Light Green
    if (probability > 0.4) return '#ffa726'; // Orange
    if (probability > 0.2) return '#ef6c00'; // Dark Orange
    return '#d32f2f'; // Red
  };

  const drawerContent = (
    <Box sx={{ width: 250 }} role="presentation">
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" color="primary">Sombra Recruitment</Typography>
        <Typography variant="body2" color="text.secondary">
          {user?.email}
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem button onClick={() => navigateTo('/dashboard')}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button onClick={() => navigateTo('/candidates')}>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText primary="Candidates" />
        </ListItem>
        <ListItem button selected onClick={() => navigateTo('/job-vacancies')}>
          <ListItemIcon>
            <WorkIcon color="primary" />
          </ListItemIcon>
          <ListItemText primary="Job Vacancies" />
        </ListItem>
      </List>
      <Divider />
      <List>
        <ListItem button onClick={logout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
      </List>
    </Box>
  );

  const renderDetailItem = (label, value, icon = null) => (
    <Box sx={{ mb: 2 }}>
      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
        {icon && <Box component="span" sx={{ verticalAlign: 'middle', mr: 1 }}>{icon}</Box>}
        {label}
      </Typography>
      <Typography variant="body1">
        {value || 'N/A'}
      </Typography>
    </Box>
  );

  const renderCandidateResults = () => {
    if (!searchSuccess || topCandidates.length === 0) {
      return null;
    }

    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Found {foundCount} Top Candidates
        </Typography>
        
        {topCandidates.map((candidate) => (
          <Accordion key={candidate.id} sx={{ mb: 1 }}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`candidate-${candidate.id}-content`}
              id={`candidate-${candidate.id}-header`}
            >
              <Grid container alignItems="center">
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">
                    {candidate.nome}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Code: {candidate.codigo_profissional}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="body2" color="text.secondary">
                    {candidate.area_atuacao || 'Area not specified'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={candidate.similarity || 0} 
                        sx={{ 
                          height: 8, 
                          borderRadius: 5,
                          backgroundColor: '#e0e0e0',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getSimilarityColor(candidate.similarity || 0)
                          }
                        }}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {Math.round(candidate.similarity || 0)}%
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </AccordionSummary>
            <AccordionDetails>
              <Box>
                <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                      variant="contained"
                      size="small"
                      color="secondary"
                      startIcon={<Insights />}
                      onClick={() => getOfferChances(candidate.id, candidate.codigo_profissional)}
                      disabled={loadingOfferChances[candidate.id]}
                    >
                      Offer Chances
                    </Button>
                    <Button
                      variant="contained"
                      size="small"
                      color="primary"
                      startIcon={<PsychologyIcon />}
                      onClick={() => analyzeCandidateCV(candidate.id, candidate.similarity)}
                      disabled={loadingCvAnalysis[candidate.id]}
                    >
                      Analyze CV
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<VisibilityIcon />}
                      onClick={() => navigateTo(`/candidates/${candidate.id}`)}
                    >
                      View Profile
                    </Button>
                  </Box>
                  
                  {/* Offer Chances Result Display */}
                  {loadingOfferChances[candidate.id] ? (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <CircularProgress size={20} sx={{ mr: 1 }} />
                      <Typography variant="body2">Calculating offer chances...</Typography>
                    </Box>
                  ) : offerChances[candidate.id] !== undefined ? (
                    offerChances[candidate.id] >= 0 ? (
                      <Tooltip title="Probability that the candidate will accept an offer">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Typography variant="body2" sx={{ mr: 1 }}>Acceptance Probability:</Typography>
                          <Chip 
                            label={`${Math.round(offerChances[candidate.id] * 100)}%`}
                            sx={{ 
                              backgroundColor: getAcceptanceProbabilityColor(offerChances[candidate.id]),
                              color: 'white',
                              fontWeight: 'bold'
                            }}
                          />
                        </Box>
                      </Tooltip>
                    ) : (
                      <Typography variant="body2" color="error">
                        Error calculating offer chances
                      </Typography>
                    )
                  ) : null}
                </Box>

                {/* CV Analysis Section */}
                {loadingCvAnalysis[candidate.id] && (
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', my: 3 }}>
                    <CircularProgress size={40} sx={{ mb: 2 }} />
                    <Typography variant="body1" align="center">
                      Analyzing CV with SombraLLM 🐕...
                    </Typography>
                    <Typography variant="body2" color="text.secondary" align="center">
                      This may take a moment. Please be patient.
                    </Typography>
                  </Box>
                )}

                {cvAnalysis[candidate.id] && !loadingCvAnalysis[candidate.id] && (
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                      <PsychologyIcon sx={{ mr: 1 }} /> SombraLLM Analysis
                    </Typography>
                    <Paper 
                      variant="outlined" 
                      sx={{ 
                        p: 2, 
                        backgroundColor: '#f5f5f5',
                        borderLeft: '4px solid #3f51b5',
                        whiteSpace: 'pre-line'
                      }}
                    >
                      {cvAnalysis[candidate.id]}
                    </Paper>
                  </Box>
                )}

                <Typography variant="subtitle2" gutterBottom>
                  Resume Highlights:
                </Typography>
                <Paper 
                  variant="outlined" 
                  sx={{ 
                    p: 2, 
                    maxHeight: '300px', 
                    overflow: 'auto',
                    whiteSpace: 'pre-line',
                    backgroundColor: '#f9f9f9',
                    fontFamily: 'monospace'
                  }}
                >
                  {candidate.cv_pt || 'No resume available'}
                </Paper>
              </Box>
            </AccordionDetails>
          </Accordion>
        ))}
      </Box>
    );
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={toggleDrawer}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Job Vacancy Details
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer}
      >
        {drawerContent}
      </Drawer>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          backgroundColor: (theme) => theme.palette.background.default,
          minHeight: '100vh'
        }}
      >
        <Container maxWidth="lg">
          <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
            <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>
              Dashboard
            </Link>
            <Link to="/job-vacancies" style={{ textDecoration: 'none', color: 'inherit' }}>
              Job Vacancies
            </Link>
            <Typography color="text.primary">Details</Typography>
          </Breadcrumbs>
          
          <Box sx={{ mb: 3, display: 'flex', alignItems: 'center' }}>
            <Button 
              startIcon={<ArrowBackIcon />} 
              onClick={() => navigate('/job-vacancies')}
              sx={{ mr: 2 }}
            >
              Back to Vacancies
            </Button>
          </Box>
          
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}
          
          {loading ? (
            <Box display="flex" justifyContent="center" my={5}>
              <CircularProgress />
            </Box>
          ) : vacancy ? (
            <>
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h4" gutterBottom>
                  {vacancy.titulo_vaga}
                </Typography>
                
                <Stack direction="row" spacing={1} sx={{ mb: 3 }}>
                  <Chip 
                    icon={<BusinessIcon />} 
                    label={vacancy.cliente} 
                    color="primary" 
                    variant="outlined" 
                  />
                  <Chip 
                    icon={<LocationIcon />} 
                    label={`${vacancy.cidade}, ${vacancy.estado}, ${vacancy.pais}`} 
                    variant="outlined" 
                  />
                  <Chip 
                    icon={<CalendarIcon />} 
                    label={formatDate(vacancy.data_requicisao)} 
                    variant="outlined" 
                  />
                  <Chip 
                    icon={<AssignmentIcon />} 
                    label={`ID: ${vacancy.vaga_id}`} 
                    variant="outlined" 
                  />
                </Stack>
                
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Card variant="outlined" sx={{ height: '100%' }}>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Basic Information
                        </Typography>
                        {renderDetailItem('Client', vacancy.cliente)}
                        {renderDetailItem('Client Requester', vacancy.solicitante_cliente)}
                        {renderDetailItem('Company Division', vacancy.empresa_divisao)}
                        {renderDetailItem('Requester', vacancy.requisitante)}
                        {renderDetailItem('Responsible Analyst', vacancy.analista_responsavel)}
                        {renderDetailItem('Hiring Type', vacancy.tipo_contratacao)}
                        {renderDetailItem('Location', `${vacancy.cidade}, ${vacancy.estado}, ${vacancy.pais}`)}
                      </CardContent>
                    </Card>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Card variant="outlined" sx={{ height: '100%' }}>
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Requirements
                        </Typography>
                        {renderDetailItem('Professional Level', vacancy.nivel_profissional)}
                        {renderDetailItem('Academic Level', vacancy.nivel_academico)}
                        {renderDetailItem('English Level', vacancy.nivel_ingles)}
                        {renderDetailItem('Spanish Level', vacancy.nivel_espanhol)}
                        {renderDetailItem('Areas of Expertise', vacancy.areas_atuacao)}
                        {renderDetailItem('PCD Specific Vacancy', vacancy.vaga_especifica_para_pcd)}
                        {renderDetailItem('Required Travel', vacancy.viagens_requeridas || 'None')}
                        {renderDetailItem('Required Equipment', vacancy.equipamentos_necessarios || 'None')}
                      </CardContent>
                    </Card>
                  </Grid>
                  
                  <Grid item xs={12}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Main Activities
                        </Typography>
                        <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                          {vacancy.principais_atividades || 'No information provided.'}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  
                  <Grid item xs={12}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Technical and Behavioral Skills
                        </Typography>
                        <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                          {vacancy.competencia_tecnicas_e_comportamentais || 'No information provided.'}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  
                  <Grid item xs={12}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Additional Observations
                        </Typography>
                        <Typography variant="body1">
                          {vacancy.demais_observacoes || 'No additional observations.'}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          Find Top Candidates
                        </Typography>
                        <Typography variant="body1" paragraph>
                          Search for candidates that best match this job vacancy based on the job description.
                        </Typography>
                        
                        <Box sx={{ mb: 3 }}>
                          <Typography variant="subtitle2" gutterBottom>
                            Number of candidates to find:
                          </Typography>
                          <ToggleButtonGroup
                            value={topCandidatesCount}
                            exclusive
                            onChange={handleTopCandidatesCountChange}
                            aria-label="number of top candidates"
                            sx={{ mb: 2 }}
                          >
                            <ToggleButton value={5} aria-label="5 candidates">
                              5
                            </ToggleButton>
                            <ToggleButton value={10} aria-label="10 candidates">
                              10
                            </ToggleButton>
                            <ToggleButton value={25} aria-label="25 candidates">
                              25
                            </ToggleButton>
                          </ToggleButtonGroup>
                          
                          <Button
                            variant="contained"
                            startIcon={<SearchIcon />}
                            onClick={searchTopCandidates}
                            disabled={searchingCandidates}
                          >
                            Search Top Candidates
                          </Button>
                        </Box>
                        
                        {searchError && (
                          <Alert severity="error" sx={{ mb: 3 }}>
                            {searchError}
                          </Alert>
                        )}
                        
                        {searchingCandidates ? (
                          <Box display="flex" flexDirection="column" alignItems="center" my={3}>
                            <CircularProgress size={60} sx={{ mb: 2 }} />
                            <Typography variant="body1">
                              Searching for the best candidates... This may take a moment.
                            </Typography>
                          </Box>
                        ) : (
                          renderCandidateResults()
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>
            </>
          ) : (
            <Alert severity="info">No vacancy found with the provided ID.</Alert>
          )}
        </Container>
      </Box>
    </Box>
  );
};

export default JobVacancyDetailPage;
