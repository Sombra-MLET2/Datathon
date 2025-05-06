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
  Breadcrumbs
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
  Assignment as AssignmentIcon
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
        <ListItem button onClick={() => navigateTo('/applicants')}>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText primary="Applicants" />
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
